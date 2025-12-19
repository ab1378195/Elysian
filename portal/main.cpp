#include <windows.h>
#include <shellscalingapi.h>
#pragma comment(lib, "Shcore.lib")

#include <onnxruntime_cxx_api.h>
#include <opencv2/opencv.hpp>

#include <iostream>
#include <vector>
#include <unordered_map>
#include <array>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
namespace py = pybind11;

struct Box {
    float x;
    float y;
    float w;
    float h;
};

struct Point {
    float x;
    float y;
};

using InternalResult = std::unordered_map<std::string, std::vector<Point>>;
using PyResultDict = std::unordered_map<std::string, std::vector<std::pair<float, float>>>;

static const std::vector<std::string> CLASS_NAMES = {
    "Elysia", "Mobius", "Pardofelis", "Boss", "Lock",
    "Aponia", "Vill_V", "Kosma", "Kevin", "Kalpas",
    "Store", "Eden", "Su", "Hua", "Griseo", "Sakura"
};


bool CaptureWindow(HWND hwnd, cv::Mat& out_img)
{
    RECT rc;
    GetWindowRect(hwnd, &rc);
    int width = rc.right - rc.left;
    int height = rc.bottom - rc.top;

    HDC hdcWindow = GetDC(hwnd);
    HDC hdcMem = CreateCompatibleDC(hdcWindow);

    HBITMAP hBitmap = CreateCompatibleBitmap(
        hdcWindow, width, height
    );
    SelectObject(hdcMem, hBitmap);

    BOOL ok = PrintWindow(hwnd, hdcMem, 0);

    BITMAP bmp;
    GetObject(hBitmap, sizeof(BITMAP), &bmp);

    cv::Mat img(height, width, CV_8UC4);
    GetBitmapBits(
        hBitmap,
        bmp.bmHeight * bmp.bmWidthBytes,
        img.data
    );

    cv::cvtColor(img, out_img, cv::COLOR_BGRA2BGR);

    DeleteObject(hBitmap);
    DeleteDC(hdcMem);
    ReleaseDC(hwnd, hdcWindow);

    return ok;
}

cv::Mat Preprocess(const cv::Mat& src,
    int w, int h)
{
    cv::Mat resized;
    cv::resize(src, resized, cv::Size(w, h));
    cv::cvtColor(resized, resized, cv::COLOR_BGR2RGB);
    resized.convertTo(resized, CV_32F, 1.0 / 255.0);
    return resized;
}

float IoU(const Box& a, const Box& b)
{
    float ax1 = a.x - a.w / 2;
    float ay1 = a.y - a.h / 2;
    float ax2 = a.x + a.w / 2;
    float ay2 = a.y + a.h / 2;

    float bx1 = b.x - b.w / 2;
    float by1 = b.y - b.h / 2;
    float bx2 = b.x + b.w / 2;
    float by2 = b.y + b.h / 2;

    float inter_x1 = std::max(ax1, bx1);
    float inter_y1 = std::max(ay1, by1);
    float inter_x2 = std::min(ax2, bx2);
    float inter_y2 = std::min(ay2, by2);

    float inter_w = std::max(0.f, inter_x2 - inter_x1);
    float inter_h = std::max(0.f, inter_y2 - inter_y1);
    float inter_area = inter_w * inter_h;

    float area_a = a.w * a.h;
    float area_b = b.w * b.h;

    return inter_area / (area_a + area_b - inter_area + 1e-6f);
}


std::vector<Box> NMS(
    const std::vector<Box>& boxes,
    float iou_thres = 0.45f
) {
    std::vector<Box> result;
    std::vector<bool> removed(boxes.size(), false);

    for (size_t i = 0; i < boxes.size(); ++i) {
        if (removed[i]) continue;

        result.push_back(boxes[i]);

        for (size_t j = i + 1; j < boxes.size(); ++j) {
            if (removed[j]) continue;

            if (IoU(boxes[i], boxes[j]) > iou_thres) {
                removed[j] = true;
            }
        }
    }
    return result;
}


InternalResult RunYolo(
    Ort::Session& session,
    const cv::Mat& frame,
    float conf_thres = 0.25f
) {
    constexpr int INPUT_W = 640;
    constexpr int INPUT_H = 640;
    constexpr int NUM_CLASSES = 16;

    cv::Mat img = Preprocess(frame, INPUT_W, INPUT_H);

    // HWC → CHW
    std::vector<float> input_tensor(3 * INPUT_W * INPUT_H);
    int idx = 0;
    for (int c = 0; c < 3; ++c)
        for (int y = 0; y < INPUT_H; ++y)
            for (int x = 0; x < INPUT_W; ++x)
                input_tensor[idx++] =
                img.at<cv::Vec3f>(y, x)[c];

    Ort::AllocatorWithDefaultOptions allocator;
    std::array<int64_t, 4> shape{ 1, 3, INPUT_H, INPUT_W };

    Ort::Value input = Ort::Value::CreateTensor<float>(
        allocator.GetInfo(),
        input_tensor.data(),
        input_tensor.size(),
        shape.data(),
        shape.size()
    );

    auto input_name = session.GetInputNameAllocated(0, allocator);
    auto output_name = session.GetOutputNameAllocated(0, allocator);

    const char* input_names[] = { input_name.get() };
    const char* output_names[] = { output_name.get() };

    auto outputs = session.Run(
        Ort::RunOptions{ nullptr },
        input_names,
        &input,
        1,
        output_names,
        1
    );

    float* out = outputs[0].GetTensorMutableData<float>();
    auto out_shape =
        outputs[0].GetTensorTypeAndShapeInfo().GetShape();

    int num_preds = out_shape[2];

    // ===== 内部：按 class 存 Box（用于 NMS）=====
    std::unordered_map<int, std::vector<Box>> boxes_by_class;

    float scale_x = static_cast<float>(frame.cols) / INPUT_W;
    float scale_y = static_cast<float>(frame.rows) / INPUT_H;

    for (int i = 0; i < num_preds; ++i) {
        int best_cls = -1;
        float best_score = 0.f;

        for (int c = 0; c < NUM_CLASSES; ++c) {
            float s = out[(4 + c) * num_preds + i];
            if (s > best_score) {
                best_score = s;
                best_cls = c;
            }
        }

        if (best_score < conf_thres)
            continue;

        Box b;
        b.x = out[0 * num_preds + i] * scale_x;
        b.y = out[1 * num_preds + i] * scale_y;
        b.w = out[2 * num_preds + i] * scale_x;
        b.h = out[3 * num_preds + i] * scale_y;

        boxes_by_class[best_cls].push_back(b);
    }

    // ===== 对外结果：Point + 类名 =====
    InternalResult result;

    for (auto& [cls_id, boxes] : boxes_by_class) {
        // NMS 仍然基于 Box
        auto kept = NMS(boxes, 0.45f);

        const std::string& cls_name = CLASS_NAMES[cls_id];
        auto& points = result[cls_name];

        for (const auto& b : kept) {
            points.push_back(Point{ b.x, b.y });
        }
    }

    return result;
}


class YoloDetector {
public:
    YoloDetector(const std::wstring& model_path,
        const std::wstring& window_title)
        : env(ORT_LOGGING_LEVEL_WARNING, "yolo"),
        windowTitle(window_title)
    {
        SetProcessDpiAwarenessContext(
            DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2
        );

        Ort::SessionOptions opts;
        opts.SetIntraOpNumThreads(1);
        opts.SetGraphOptimizationLevel(
            GraphOptimizationLevel::ORT_ENABLE_BASIC
        );

        session = std::make_unique<Ort::Session>(
            env,
            model_path.c_str(),
            opts
        );
    }

    PyResultDict infer() {
        HWND hwnd = FindWindowW(nullptr, windowTitle.c_str());
        if (!hwnd)
            throw std::runtime_error("Window not found");

        cv::Mat frame;
        if (!CaptureWindow(hwnd, frame))
            throw std::runtime_error("Capture failed");

        auto internal = RunYolo(*session, frame);

        PyResultDict py_result;
        for (auto& [cls, points] : internal) {
            auto& vec = py_result[cls];
            for (const auto& p : points) {
                vec.emplace_back(p.x, p.y);  // ★ tuple
            }
        }
        return py_result;
    }


private:
    Ort::Env env;
    std::unique_ptr<Ort::Session> session;
    std::wstring windowTitle;
};

PYBIND11_MODULE(portal, m) {
    m.doc() = "YOLO window inference module";

    py::class_<YoloDetector>(m, "YoloDetector")
        .def(py::init<
            const std::wstring&,
            const std::wstring&>(),
            py::arg("model_path"),
            py::arg("window_title"))
        .def("infer", &YoloDetector::infer);
}

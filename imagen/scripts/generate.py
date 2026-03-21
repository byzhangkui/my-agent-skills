#!/usr/bin/env python3
"""Generate images using Google Gemini/Imagen API."""

import argparse
import base64
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

# Model presets: generateContent models vs predict (Imagen) models
GENERATE_CONTENT_MODELS = {
    "gemini-3-pro-image-preview",
    "gemini-3.1-flash-image-preview",
    "gemini-2.5-flash-image",
}

DEFAULT_MODEL = "gemini-3-pro-image-preview"


def _call_generate_content(prompt: str, model: str) -> bytes | None:
    """Call generateContent API (Gemini image models)."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": f"Generate an image: {prompt}"}]}],
        "generationConfig": {"responseModalities": ["image", "text"]},
    }
    req = Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(req, timeout=180) as resp:
        result = json.loads(resp.read())
    for candidate in result.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            if "inlineData" in part:
                img_b64 = part["inlineData"].get("data") or part["inlineData"].get("bytesBase64Encoded")
                if img_b64:
                    return base64.b64decode(img_b64)
    return None


def _call_predict(prompt: str, model: str, aspect_ratio: str, count: int) -> list[bytes]:
    """Call predict API (Imagen models)."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:predict?key={API_KEY}"
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {"sampleCount": min(count, 4), "aspectRatio": aspect_ratio},
    }
    req = Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(req, timeout=180) as resp:
        result = json.loads(resp.read())
    images = []
    for pred in result.get("predictions", []):
        image_data = pred.get("bytesBase64Encoded")
        if image_data:
            images.append(base64.b64decode(image_data))
    return images


def generate_image(prompt: str, output_dir: str, aspect_ratio: str = "1:1",
                   count: int = 1, model: str = DEFAULT_MODEL, filename: str | None = None) -> list[str]:
    """Generate images and save to output_dir."""
    if not API_KEY:
        print("Error: 请设置环境变量 GEMINI_API_KEY 或 GOOGLE_API_KEY", file=sys.stderr)
        print("获取方式: https://aistudio.google.com/apikey", file=sys.stderr)
        sys.exit(1)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    saved_files = []

    try:
        if model in GENERATE_CONTENT_MODELS:
            # generateContent models generate one image per call
            for i in range(count):
                img_data = _call_generate_content(prompt, model)
                if not img_data:
                    print(f"Warning: 第 {i+1} 张未返回图片", file=sys.stderr)
                    continue
                if filename and count == 1:
                    fname = filename
                elif filename:
                    stem = Path(filename).stem
                    ext = Path(filename).suffix or ".png"
                    fname = f"{stem}_{i+1}{ext}"
                else:
                    suffix = f"_{i+1}" if count > 1 else ""
                    fname = f"imagen_{timestamp}{suffix}.png"
                filepath = output_path / fname
                filepath.write_bytes(img_data)
                saved_files.append(str(filepath))
                print(f"Saved: {filepath}")
        else:
            # Imagen predict API supports batch generation
            images = _call_predict(prompt, model, aspect_ratio, count)
            if not images:
                print("Error: API 未返回任何图片", file=sys.stderr)
                sys.exit(1)
            for i, img_data in enumerate(images):
                if filename and len(images) == 1:
                    fname = filename
                elif filename:
                    stem = Path(filename).stem
                    ext = Path(filename).suffix or ".png"
                    fname = f"{stem}_{i+1}{ext}"
                else:
                    suffix = f"_{i+1}" if count > 1 else ""
                    fname = f"imagen_{timestamp}{suffix}.png"
                filepath = output_path / fname
                filepath.write_bytes(img_data)
                saved_files.append(str(filepath))
                print(f"Saved: {filepath}")

    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"API Error ({e.code}): {body}", file=sys.stderr)
        sys.exit(1)

    return saved_files


def main():
    parser = argparse.ArgumentParser(description="Generate images with Google AI")
    parser.add_argument("prompt", help="Image generation prompt")
    parser.add_argument("-o", "--output", default=".", help="Output directory")
    parser.add_argument("-r", "--ratio", default="1:1",
                        choices=["1:1", "3:4", "4:3", "9:16", "16:9"],
                        help="Aspect ratio (default: 1:1)")
    parser.add_argument("-n", "--count", type=int, default=1,
                        choices=[1, 2, 3, 4], help="Number of images (default: 1)")
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL,
                        help=f"Model name (default: {DEFAULT_MODEL})")
    parser.add_argument("-f", "--filename", default=None,
                        help="Custom output filename (e.g. my-image.png)")
    args = parser.parse_args()

    generate_image(args.prompt, args.output, args.ratio, args.count, args.model, args.filename)


if __name__ == "__main__":
    main()

# 构建 CLI 可执行文件

VideoCaptioner 支持通过 PyInstaller 打包为独立的可执行文件，用户无需安装 Python 或执行 `pip install`。

## 前置条件

- Python >= 3.10
- 项目依赖已安装：`pip install -e .`

## 快速构建

```bash
# 安装 PyInstaller
pip install pyinstaller

# 构建
pyinstaller videocaptioner.spec --noconfirm

# 复制资源文件到 dist
cp -r resource/subtitle_style dist/videocaptioner/resource/
cp -r resource/fonts dist/videocaptioner/resource/
mkdir -p dist/videocaptioner/resource/bin
```

构建完成后，可执行文件位于 `dist/videocaptioner/videocaptioner.exe`（Windows）或 `dist/videocaptioner/videocaptioner`（macOS/Linux）。

## 使用构建脚本

```bash
python scripts/build_exe.py          # 构建
python scripts/build_exe.py --clean  # 清理后构建
```

构建脚本自动完成：依赖检查、PyInstaller 构建、资源文件复制、bin 目录创建。

## 产物结构

```
dist/videocaptioner/
  videocaptioner.exe          # 入口可执行文件
  _internal/                  # Python 运行时 + 依赖
  resource/
    fonts/                    # 字体文件
    subtitle_style/           # 字幕样式 JSON
    bin/                      # 外部二进制（用户自行放入）
      README.txt
```

## 外部二进制

以下二进制不与可执行文件一起分发，需由用户自行放入 `resource/bin/`：

| 二进制 | 用途 | 必需 |
|--------|------|------|
| `ffmpeg` | 音视频处理、字幕合成 | 是（synthesize / 部分 ASR） |
| `yt-dlp` | 在线视频下载 | 否 |
| `whisper-cpp` | 本地 ASR（`--asr whisper-cpp`） | 否 |
| `faster-whisper-xxl` | 本地 ASR（快速变体） | 否 |

`bijian` / `jianying` ASR 和 LLM 优化/翻译不需要任何外部二进制。

## 配置与缓存

可执行文件使用标准系统目录存储配置和缓存：

| 目录 | 路径 |
|------|------|
| 配置 | `~/.config/videocaptioner/config.toml` (Linux/macOS) |
| 缓存 | 系统用户数据目录下的 `VideoCaptioner/cache/` |
| 工作 | `~/VideoCaptioner/` |

配置优先级：命令行参数 > 环境变量 > 配置文件。

## CI 构建（GitHub Actions）

在 Actions 页面手动触发 `Build standalone executables` workflow，可选填写版本号（留空则使用 `0.0.0-ci`）。

矩阵覆盖五个平台：

| Platform | Runner |
|----------|--------|
| Windows x86-64 | `windows-latest` |
| Windows arm64 | `windows-11-arm` |
| Linux x86-64 | `ubuntu-latest` |
| Linux arm64 | `ubuntu-24.04-arm` |
| macOS arm64 | `macos-latest` |

构建完成后从 Actions 页面下载对应平台的 artifact。

## 注意事项

- 当前仅构建 CLI（命令行），不含 GUI（PyQt5 相关模块已在 spec 文件中排除）
- 打包后的可执行文件约 80 MB（含 Python 运行时及所有依赖）
- macOS 用户首次运行可能需通过 Gatekeeper：`xattr -d com.apple.quarantine videocaptioner`
- `_version.py` 在非 hatch 构建环境下会自动生成占位版本号

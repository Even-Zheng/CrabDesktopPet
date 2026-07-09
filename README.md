# CrabDesktopPet
一个非常粗制滥造的螃蟹cc自制桌宠罢了。。

# Crab Pet 螃蟹桌宠 v1.0

A desktop pet crab that lives on your taskbar with idle animations, walking, running, and interactive responses.

## 下载运行

1. 去 [Releases 页面](../../releases) 下载 `CrabPet_v1.0.exe`
2. 下载 `assets.zip` 并解压到 EXE 同级目录
3. 双击 `CrabPet_v1.0.exe` 运行
## 功能说明

### 常态行为
- 桌宠始终处于屏幕范围内，不会超出边界
- 未交互时停留在屏幕最下端任务栏上方

### 待机状态（Await）
- 长时间（10秒）未交互时，50%概率进入 Await 状态
- 在 Await_1 ~ Await_5 之间随机播放，每个状态持续10秒

### 移动状态（Walk & Run）
- 长时间（10秒）未交互时，50%概率进入 Walk/Run 状态
- **Walk**：速度慢，移动约半屏距离后停止
- **Run**：速度快，移动约全屏距离后停止
- 到达边界自动回头，结束后重新判定下一状态

### 交互状态

| 交互方式 | 触发条件 | 效果 |
|---------|---------|------|
| Click（点击） | 鼠标左键短按 | 随机播放 Click_1 或 Click_2，持续8秒 |
| Catch（拖拽） | 鼠标左键长按移动 | 播放 Catch.gif，可拖拽到任意位置 |
| Drop（下落） | 松开拖拽后 | 播放 Drop.gif，自由落体到任务栏 |
| 右键菜单 | 鼠标右键点击 | 显示菜单，可选择退出 |

### 退出
- 右键菜单选择"Exit"
- 播放 Bye.gif 6秒后关闭进程

## 文件结构
dist/
├── CrabPet_v1.0.exe    # 主程序
├── assets/             # GIF 资源文件夹
│   ├── await/          # 待机动画 x5
│   ├── walk/           # 行走动画
│   ├── run/            # 奔跑动画
│   ├── click/          # 点击反馈 x2
│   ├── catch/          # 拖拽动画
│   ├── drop/           # 下落动画
│   └── bye/            # 退出动画


## 技术栈

- Python 3.14
- PyQt6
- PyInstaller

## 开发环境

- VS2022 + Python Tools

## 项目文件

| 文件 | 说明 |
|------|------|
| `launcher.py` | 程序入口 |
| `main.py` | 主循环 |
| `config.py` | 全局配置 |
| `window.py` | 无边框窗口 |
| `animator.py` | 动画状态机 |
| `mover.py` | 移动逻辑 |
| `interaction.py` | 鼠标交互 |
| `idle_system.py` | 待机系统 |

##现有问题
功能较少
长时间运行可能会有闪退问题
未在菜单加入调节大小和固定位置功能
转换不同状态不够平滑与灵活
现有的gif是录屏表情包制作，未去除黑框以及循环播放时的不连续问题

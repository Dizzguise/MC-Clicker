
# 🖱️ MC Clicker

A lightweight, modern autoclicker for Windows with a clean GUI. Click away without bloat!

**Features:**
- ✨ Modern, dark-themed GUI
- ⚡ Low CPU/memory footprint
- 🎯 Configurable click speed (CPS ↔ Seconds conversion)
- 🖲️ Left/Right click options
- ⌨️ Customizable hotkey (F6 default, auto-saved)
- 📦 Standalone executable (11.33 MB)
- 🔒 No dependencies, no installation needed

---

## 🚀 Quick Start

### For Users (Running the App)

1. Download `MCClicker.exe` from [Releases](https://github.com/Dizzguise/MC-Clicker/tree/main/dist)
2. Run the .exe - **no installation needed!**
3. Configure your settings:
   - **Click Speed**: Default 1.6 CPS (perfect for Minecraft)
   - **Click Button**: Choose Left or Right click
   - **Hotkey**: Click "Change", press your desired key
4. Press your hotkey to toggle clicking on/off

**That's it!** Settings are automatically saved.

### Tips:
- Hotkey toggles clicking on/off
- All settings apply instantly
- Your hotkey is remembered next time you run it
- Some systems require **administrator rights** for global hotkeys

---

## 📋 Requirements

- **OS**: Windows 10 or 11 (64-bit)
- **Disk**: ~15 MB free
- **That's all!** No Python, no dependencies.

---

## 🛠️ For Developers

### Setup

```bash
# Clone the repo
git clone https://github.com/YOUR-USERNAME/MC-Clicker.git
cd MC-Clicker

# Install dependencies
pip install -r requirements.txt

# Run the app
python -m src.main

# Run tests
pytest tests/ -v

# Build executable
python build/build.py
```

### Project Structure

```
MC-Clicker/
├── src/
│   ├── main.py           # GUI application
│   ├── clicker.py        # Mouse clicking logic
│   ├── hotkey.py         # Global hotkey manager
│   └── utils.py          # Utility functions
├── tests/
│   ├── test_clicker.py   # Clicker tests
│   ├── test_hotkey.py    # Hotkey tests
│   └── test_utils.py     # Utility tests
├── build/
│   └── build.py          # PyInstaller build script
├── dist/
│   └── MCClicker.exe     # Standalone executable
├── README.md             # This file
├── PLANNING.md           # Architecture & design
├── GETTING_STARTED.md    # Quick setup guide
└── requirements.txt      # Python dependencies
```

### Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_clicker.py -v

# Current status: 51/51 tests passing
```

---

## 🎮 Usage Examples

### Minecraft AFK Mining
- Default 1.6 CPS is perfect
- Set to Left Click (default)
- Press F6 to start, F6 to stop

### Fast Clicking Challenge  
- Increase CPS to 15-20
- Left Click
- Use custom hotkey if desired

### Right-Click Spam
- Set CPS to 5-10
- Choose Right Click
- Perfect for building/testing

---

## ⚙️ Hotkey Format

Enter hotkeys in your preferred format:
- Single key: `f6`, `space`, `enter`
- With modifiers: `ctrl+f6`, `alt+f`, `shift+c`
- Multiple modifiers: `alt+shift+f6`, `ctrl+shift+f8`

**Supported keys**: F1-F12, A-Z, 0-9, Enter, Space, Tab, Esc, etc.

---

## 🐛 Troubleshooting

### Hotkey not working?
- Try running as Administrator
- Ensure the hotkey isn't bound to another application
- Some systems require admin rights for global hotkeys

### Clicks not registering?
- Make sure the game/app window is focused
- Check the status indicator shows "RUNNING"
- Try adjusting the CPS value

### GUI looks small?
- This is intentional to keep the app lightweight
- Windows scales UI automatically

---

## 📄 License

This project is provided as-is for personal use.

---

## 🚀 Contributing

Feel free to fork, modify, and use this project as you wish!

---

**Made with ❤️ using Python**




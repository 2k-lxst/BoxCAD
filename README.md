![BoxCAD Banner](assets/thin_banner.png)

# BoxCAD 📦  
## A Parametric Enclosure Designer for Makers

**BoxCAD** is a lightweight, Python-powered desktop application for designing custom, 3D-printable project enclosures. Instead of manually modeling simple boxes in CAD software, you define dimensions and hardware presets, preview the result in real time, and export directly for manufacturing.

The goal is speed, repeatability, and clean parametric control — especially for electronics projects.

---

## ✨ Key Features

- **True Parametric Design**  
  Adjust length, width, height, and wall thickness. All dependent features — lids, screw holes, offsets — update automatically.

- **Hardware Presets**  
  Built-in footprints for popular boards such as Arduino Uno, ESP32, and Raspberry Pi simplify mounting and alignment.

- **Real-time 3D Preview**  
  An OpenGL-accelerated viewport lets you instantly visualize changes as you tweak parameters.

- **Manufacturing Ready**  
  Export clean `.STL` files suitable for direct 3D printing.

---

## 🛠️ Built With

BoxCAD is built entirely in Python using modern, well-supported libraries:

- **Python 3.14.2**
- **PySide6** – Native-looking cross-platform GUI
- **CadQuery** – Industrial-grade parametric geometry kernel
- **PyQtGraph** – High-performance 3D visualization

---

## 🚀 Getting Started

## 1. Installation & usage
You can install and run BoxCAD by simply extracting the .zip file, going into the extracted folder and running the .exe file.

The welcome window will open, in which you can create a project, browse the hardware library and watch tutorials.

---

## 🏞️ Short demo GIF
Below is a short GIF showing the functionality so far.
![BoxCAD demo](assets/demo/demo.gif)

## 📄 License

This project uses the *MIT License*. You can learn more about it [here](https://github.com/2k-lxst/BoxCAD/blob/main/LICENSE).

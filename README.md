# UPS Container Tracking System

A camera-based system that automatically identifies, tracks, and prioritizes shipping containers at a warehouse facility using Optical Character Recognition (OCR) and a MySQL database.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Directory Structure](#directory-structure)
- [Modules](#modules)
- [Data Flow](#data-flow)
- [Database Schema](#database-schema)
- [Setup & Installation](#setup--installation)
- [Running the Application](#running-the-application)
- [Known Issues](#known-issues)

---

## Overview

When a shipping container arrives at a warehouse, a webcam captures an image of the container's label. The system reads the UPS container ID from that label using OCR, looks up the container's metadata (fragility, priority, contents) in a MySQL database, and displays a pop-up alert to warehouse staff with handling instructions.

---

## Architecture

```
Webcam → fswebcam → image.jpg
                        │
                   ExtractText.py  (OpenCV + Tesseract OCR)
                        │
                  Container ID string
                        │
              DatabaseController.py  (MySQLdb)
                        │
                  Container object
                        │
               ContainerAlert.py  (Tkinter GUI)
                        │
               Alert pop-up on screen
```

**Technology Stack:**

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Image capture | `fswebcam` (Linux CLI tool) |
| Image processing | OpenCV (`cv2`), NumPy, Pillow |
| OCR | Tesseract via `pytesseract` |
| Database | MySQL / MariaDB |
| Database driver | `MySQLdb` |
| GUI alerts | Tkinter |
| Deployment target | Linux with a connected webcam |

---

## Directory Structure

```
ContainerTracking/
├── ImageToText/
│   ├── UPSController.py        Main entry point – orchestrates the pipeline
│   ├── ExtractText.py          OCR and adaptive image processing
│   ├── DatabaseController.py   Database queries and Container data model
│   └── ContainerAlert.py       Tkinter pop-up alert window
│
├── Database/
│   ├── upsdemodump.sql         MySQL demo database dump (MariaDB 10.0.31)
│   ├── dump-upscontainertrackingdb-201712090501.sql  Full MySQL backup
│   ├── UPS Database.sql        Alternative SQL Server schema
│   └── Database_readme.txt     Placeholder notes
│
└── ContainerTracking.wiki/     Empty wiki directory
```

---

## Modules

### `UPSController.py` — Main Orchestrator

Entry point for the application. Run this file to start the system.

- Invokes `fswebcam` to capture a 352×288 JPEG image from the webcam.
- Calls `ExtractText.readImg()` to extract the container ID from the image.
- Retrieves the network interface MAC address (used as the camera identifier).
- Opens a `DatabaseController`, updates the container's camera location, and retrieves the container's metadata.
- Calls `ContainerAlert.alertPopUp()` to display the alert.
- Times each stage and prints elapsed seconds.

> **Note:** Database credentials (`host`, `db`, `user`, `passwd`) are currently hardcoded. A TODO comment in the file notes they should be moved to an encrypted config file.

---

### `ExtractText.py` — OCR & Image Processing

Responsible for turning a raw webcam image into a validated container ID string.

**`readImg(img)`** — public entry point  
Applies an initial bilateral filter to reduce noise, then attempts OCR up to four times with different filter parameters. Returns the extracted text and the number of attempts made.

**`extract(img, d, sigmaColor, sigmaSpace)`** — core OCR pipeline  
1. Denoises with `cv2.fastNlMeansDenoisingColored`  
2. Converts to grayscale and applies bilateral filtering  
3. Detects edges with Canny, then finds contours to locate the label region  
4. Crops the image to the label, applies further denoising and thresholding  
5. Runs Tesseract OCR and strips non-alphanumeric characters from the result

**`check(text)`** — validation  
Validates the extracted string against the expected UPS label format:  
`[A-Z0-9]{7,8}UPS`  
Returns `True` if valid, `False` otherwise. If all four attempts fail, `readImg` returns `"UnreadableContainer"`.

**Adaptive filter parameters tried in order:**

| Attempt | d | sigmaColor | sigmaSpace |
|---|---|---|---|
| 0 | 7 | 150 | 115 |
| 1 | 7 | 50 | 50 |
| 2 | 6 | 50 | 50 |
| 3 | 9 | 75 | 75 |

---

### `DatabaseController.py` — Database Operations

Manages all MySQL interactions and defines the in-memory `Container` data model.

**`DatabaseCredentials`** — simple value object holding `host`, `db`, `user`, `passwd`.

**`DatabaseController`**  
- `__init__(credentials)` — opens a `MySQLdb` connection.  
- `retrieveContainer(containerID)` — `SELECT * FROM CONTAINERS WHERE ID = ...`; returns a `Container` object.  
- `updateContainer(containerID, cameraID)` — `UPDATE CONTAINERS SET CAMERA_ID = ...` to record which camera last saw the container.  
- `endConnection()` — closes the database connection.

**`Container`** — data class populated from a database row:

| Field | Type | Description |
|---|---|---|
| `containerID` | `str` | Primary key / UPS label text |
| `fragile` | `bool` | Whether the container is fragile |
| `priority` | `int` | FK → `PRIORITIES` table |
| `content` | `int` | FK → `Contents` table |
| `camID` | `str` | Camera MAC address that last scanned the container |

---

### `ContainerAlert.py` — Alert GUI

Builds and displays a Tkinter pop-up window with container handling instructions.

**`alertPopUp(container)`** — creates the Tkinter root, builds the message, shows the window, and starts the event loop.

**`messageBuilder(container)`** — constructs a human-readable message:
- Maps `content` codes to descriptions via `getContentsString()`.
- Assigns a priority label:
  - **Highest Priority** — medical/chemical/unknown contents (codes 1, 2, 6) with priority 1 or 2, or any unreadable container.
  - **Low Priority** — food (code 3).
  - **Part of Larger Order** — code 4.
  - **Temperature Sensitive** — medical or food (codes 1, 3).
  - **Fragile** note added when `container.fragile` is `True`.

**Content code → description mapping:**

| Code | Description |
|---|---|
| 1 | Medical supplies |
| 2 | Chemicals |
| 3 | Food |
| 4 | Electronics |
| 5 | Industrial components |
| 6 | Unknown |

---

## Data Flow

```
1. CAPTURE
   UPSController runs:  fswebcam -r 352x288 -S 20 --no-banner image.jpg
   Result: image.jpg written to disk

2. OCR
   ExtractText.readImg(cv2.imread("image.jpg"))
   Adaptive bilateral filtering + Canny edge detection + contour crop + Tesseract
   Result: e.g. "ABC12345UPS"  (or "UnreadableContainer" on failure)

3. VALIDATE
   ExtractText.check(text)
   Regex: [A-Z0-9]{7,8}UPS
   Result: validated container ID string

4. DATABASE UPDATE
   DatabaseController.updateContainer("ABC12345UPS", "aa:bb:cc:dd:ee:ff")
   SQL: UPDATE CONTAINERS SET CAMERA_ID='aa:bb:cc:dd:ee:ff' WHERE ID='ABC12345UPS'

5. DATABASE RETRIEVAL
   DatabaseController.retrieveContainer("ABC12345UPS")
   SQL: SELECT * FROM CONTAINERS WHERE ID='ABC12345UPS'
   Result: Container object (containerID, fragile, priority, content, camID)

6. ALERT
   ContainerAlert.alertPopUp(container)
   Result: Tkinter window displayed to warehouse staff
```

---

## Database Schema

The application ships with two schema variants (see `Database/`):

### MySQL / MariaDB (`upsdemodump.sql`)

**`CONTAINERS`**
```sql
ID          VARCHAR(100) PRIMARY KEY   -- UPS label text, e.g. ABC12345UPS
FRAGILE     TINYINT(1)  DEFAULT 0      -- 0 = not fragile, 1 = fragile
PRIORITY    INT                        -- FK → PRIORITIES(ID)
CONTENT     INT                        -- FK → Contents(ID)
CAMERA_ID   VARCHAR(100)               -- FK → CAMERA_LOCATIONS(CAMERA_ID)
```

**`PRIORITIES`**
```
1 → New
2 → High Priority
3 → Low Priority
4 → Part of large order
```

**`Contents`**
```
1 → Medical
2 → Chemical
3 → Food
4 → Electronic
5 → Industrial
```

**`CAMERA_LOCATIONS`**
```sql
CAMERA_ID   VARCHAR(100) PRIMARY KEY   -- Camera MAC address
LOCATION    VARCHAR(100)               -- Human-readable location description
```

### SQL Server (`UPS Database.sql`)

An alternative schema exists for SQL Server with tables `Container`, `LabelInfo`, `Camera`, and `Location`. The Python application currently targets MySQL only.

---

## Setup & Installation

### System Requirements (Linux)

```bash
# Webcam capture tool
sudo apt-get install fswebcam

# Tesseract OCR engine
sudo apt-get install tesseract-ocr

# MySQL / MariaDB server
sudo apt-get install mariadb-server
```

### Python Dependencies

```bash
pip install opencv-python numpy Pillow pytesseract mysqlclient
```

### Database Setup

1. Start MySQL and create the demo database:

   ```bash
   mysql -u root -p < Database/upsdemodump.sql
   ```

2. Create the application user:

   ```sql
   CREATE USER 'upsuser'@'localhost' IDENTIFIED BY 'upsuser';
   GRANT ALL PRIVILEGES ON upsdemo.* TO 'upsuser'@'localhost';
   FLUSH PRIVILEGES;
   ```

3. Populate the `CONTAINERS`, `PRIORITIES`, `Contents`, and `CAMERA_LOCATIONS` tables as needed.

---

## Running the Application

```bash
cd ImageToText
python UPSController.py
```

The script will:
1. Capture an image from the default webcam.
2. Extract and validate the container ID via OCR.
3. Update the container's camera location in the database.
4. Retrieve the container's full metadata.
5. Display a Tkinter alert window with handling instructions.

---

## Known Issues

| Issue | Location | Description |
|---|---|---|
| Hardcoded credentials | `UPSController.py` lines 30–33 | DB host, name, user, and password are hardcoded. Should be read from an encrypted config file. |
| SQL injection | `DatabaseController.py` | Queries use Python string substitution rather than parameterized queries. |
| Requires display | `ExtractText.py` | `cv2.imshow()` calls require a connected display or virtual framebuffer (`Xvfb`). |
| Typo in alert logic | `ContainerAlert.py` line 48 | Variable name `appened` should be `appended`. |
| No test suite | — | There are no automated tests. All testing is manual. |
| Linux-only | `UPSController.py`, `ExtractText.py` | Uses `fswebcam` and `/sys/class/net/` which are Linux-specific. |

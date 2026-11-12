# WHU-Hi: UAV-Borne Hyperspectral and High Spatial Resolution ($\text{H}^2$) Benchmark Datasets

**WHU-Hi** (Wuhan UAV-borne Hyperspectral Image) is a collection of benchmark datasets collected and shared by the **RSIDEA research group** of Wuhan University. Designed for precise crop classification and hyperspectral image classification studies, the research was published in *Remote Sensing of Environment*.

---

## Abstract

The WHU-Hi dataset comprises three individual UAV-borne hyperspectral datasets: **WHU-Hi-LongKou**, **WHU-Hi-HanChuan**, and **WHU-Hi-HongHu**. All datasets were acquired in farming areas featuring diverse crop types in Hubei province, China, utilizing a **Headwall Nano-Hyperspec** sensor mounted on a UAV platform. 

Compared to spaceborne and airborne platforms, unmanned aerial vehicle (UAV)-borne hyperspectral systems capture imagery with exceptionally high spatial resolution (referred to as **$\text{H}^2$ imagery**).

---

## 1. Dataset Overview & Preprocessing

Preprocessing for the WHU-Hi datasets included **radiometric calibration** and **geometric correction**, performed using the *HyperSpec* software provided by the instrument manufacturer. During radiometric calibration, raw digital number (DN) values were converted into radiance values using laboratory calibration parameters of the sensor.

### Quick Comparison

| Dataset | Acquisition Date | UAV Platform | Focal Length | Altitude | Spatial Resolution | Image Size (px) | Spectral Bands | Classes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **WHU-Hi-LongKou** | July 17, 2018 | DJI Matrice 600 Pro | 8 mm | 500 m | ~0.463 m | $550 \times 400$ | 270 (400–1000 nm) | 9 |
| **WHU-Hi-HanChuan** | June 17, 2016 | Leica Aibot X6 V1 | 17 mm | 250 m | ~0.109 m | $1217 \times 303$ | 274 (400–1000 nm) | 16 |
| **WHU-Hi-HongHu** | Nov 20, 2017 | DJI Matrice 600 Pro | 17 mm | 100 m | ~0.043 m | $940 \times 475$ | 270 (400–1000 nm) | 22 |

---

## 2. Individual Datasets

### 2.1 WHU-Hi-LongKou

* **Location:** Longkou Town, Hubei province, China
* **Acquisition Time:** July 17, 2018 (13:49 – 14:37)
* **Platform & Sensor:** DJI Matrice 600 Pro (DJI M600 Pro) + Headwall Nano-Hyperspec (8-mm focal length)
* **Weather Conditions:** Clear and cloudless, ~36°C, ~65% relative humidity
* **Flight & Image Specs:** 500 m altitude | $550 \times 400$ pixels | 270 bands (400–1000 nm) | ~0.463 m spatial resolution
* **Scene Description:** A simple agricultural scene containing six crop species: corn, cotton, sesame, broad-leaf soybean, narrow-leaf soybean, and rice.

#### Table 1: Ground-Truth Classes (WHU-Hi-LongKou)

| Class No. | Class Name | Samples |
| :---: | :--- | :---: |
| **C1** | Corn | 34,511 |
| **C2** | Cotton | 8,374 |
| **C3** | Sesame | 3,031 |
| **C4** | Broad-leaf soybean | 63,212 |
| **C5** | Narrow-leaf soybean | 4,151 |
| **C6** | Rice | 11,854 |
| **C7** | Water | 67,056 |
| **C8** | Roads and houses | 7,124 |
| **C9** | Mixed weed | 5,229 |

---

### 2.2 WHU-Hi-HanChuan

* **Location:** Hanchuan, Hubei province, China
* **Acquisition Time:** June 17, 2016 (17:57 – 18:46)
* **Platform & Sensor:** Leica Aibot X6 UAV V1 + Headwall Nano-Hyperspec (17-mm focal length)
* **Weather Conditions:** Clear and cloudless, ~30°C, ~70% relative humidity
* **Flight & Image Specs:** 250 m altitude | $1217 \times 303$ pixels | 274 bands (400–1000 nm) | ~0.109 m spatial resolution
* **Scene Description:** A rural-urban fringe zone featuring buildings, water, and cultivated land with seven crop species: strawberry, cowpea, soybean, sorghum, water spinach, watermelon, and greens. 
* **Notable Characteristic:** Because data was captured in the late afternoon when the solar elevation angle was low, the imagery contains significant shadow-covered areas.

#### Table 2: Ground-Truth Classes (WHU-Hi-HanChuan)

| Class No. | Class Name | Samples | Class No. | Class Name | Samples |
| :---: | :--- | :---: | :---: | :--- | :---: |
| **C1** | Strawberry | 44,735 | **C9** | Grass | 9,469 |
| **C2** | Cowpea | 22,753 | **C10** | Red roof | 10,516 |
| **C3** | Soybean | 10,287 | **C11** | Gray roof | 16,911 |
| **C4** | Sorghum | 5,353 | **C12** | Plastic | 3,679 |
| **C5** | Water spinach | 1,200 | **C13** | Bare soil | 9,116 |
| **C6** | Watermelon | 4,533 | **C14** | Road | 18,560 |
| **C7** | Greens | 5,903 | **C15** | Bright object | 1,136 |
| **C8** | Trees | 17,978 | **C16** | Water | 75,401 |

---

### 2.3 WHU-Hi-HongHu

* **Location:** Honghu City, Hubei province, China
* **Acquisition Time:** November 20, 2017 (16:23 – 17:37)
* **Platform & Sensor:** DJI Matrice 600 Pro + Headwall Nano-Hyperspec (17-mm focal length)
* **Weather Conditions:** Cloudy, ~8°C, ~55% relative humidity
* **Flight & Image Specs:** 100 m altitude | $940 \times 475$ pixels | 270 bands (400–1000 nm) | ~0.043 m spatial resolution
* **Scene Description:** A complex agricultural scene containing many crop classes, including distinct cultivars of the same crop type (e.g., Chinese cabbage vs. cabbage, and *Brassica chinensis* vs. small *Brassica chinensis*).

#### Table 3: Ground-Truth Classes (WHU-Hi-HongHu)

| Class No. | Class Name | Samples | Class No. | Class Name | Samples |
| :---: | :--- | :---: | :---: | :--- | :---: |
| **C1** | Red roof | 14,041 | **C12** | Brassica chinensis | 8,954 |
| **C2** | Road | 3,512 | **C13** | Small Brassica chinensis | 22,507 |
| **C3** | Bare soil | 21,821 | **C14** | Lactuca sativa | 7,356 |
| **C4** | Cotton | 163,285 | **C15** | Celtuce | 1,002 |
| **C5** | Cotton firewood | 6,218 | **C16** | Film covered lettuce | 7,262 |
| **C6** | Rape | 44,557 | **C17** | Romaine lettuce | 3,010 |
| **C7** | Chinese cabbage | 24,103 | **C18** | Carrot | 3,217 |
| **C8** | Pakchoi | 4,054 | **C19** | White radish | 8,712 |
| **C9** | Cabbage | 10,819 | **C20** | Garlic sprout | 3,486 |
| **C10** | Tuber mustard | 12,394 | **C21** | Broad bean | 1,328 |
| **C11** | Brassica parachinensis | 11,015 | **C22** | Tree | 4,040 |
# WHU-Hi: UAV-Borne Hyperspectral Datasets

WHU-Hi (Wuhan UAV-borne Hyperspectral Image) is a set of benchmark datasets put together and released by the RSIDEA research group at Wuhan University. It was built mainly for crop classification and hyperspectral image classification research, and the accompanying paper appeared in *Remote Sensing of Environment*.

## Overview

WHU-Hi is really three datasets: **LongKou**, **HanChuan**, and **HongHu**. All three were collected over farmland in Hubei province, China, using a Headwall Nano-Hyperspec sensor flown on a UAV. Because a drone flies so much lower than a satellite or a crewed aircraft, the images have very fine spatial detail. The authors call this kind of data H² imagery, short for hyperspectral and high spatial resolution.

Before release, the data went through radiometric calibration and geometric correction using HyperSpec, the software supplied by the sensor's manufacturer. During calibration, the raw digital number values were converted to radiance using the sensor's laboratory calibration parameters.

## Quick Comparison

| | LongKou | HanChuan | HongHu |
|---|---|---|---|
| Date | 17 July 2018 | 17 June 2016 | 20 Nov 2017 |
| UAV | DJI Matrice 600 Pro | Leica Aibot X6 V1 | DJI Matrice 600 Pro |
| Focal length | 8 mm | 17 mm | 17 mm |
| Flight altitude | 500 m | 250 m | 100 m |
| Spatial resolution | about 0.463 m | about 0.109 m | about 0.043 m |
| Image size | 550 × 400 | 1217 × 303 | 940 × 475 |
| Bands | 270 (400–1000 nm) | 274 (400–1000 nm) | 270 (400–1000 nm) |
| Classes | 9 | 16 | 22 |

## WHU-Hi-LongKou

This one was captured over Longkou Town on 17 July 2018, between 13:49 and 14:37. The sky was clear, with a temperature around 36°C and relative humidity near 65%. The drone was a DJI Matrice 600 Pro carrying the Nano-Hyperspec with an 8 mm lens, flying at 500 m. That gives a 550 × 400 image with 270 bands covering 400–1000 nm at roughly 0.463 m per pixel.

The scene is fairly simple. It contains six crops (corn, cotton, sesame, broad-leaf soybean, narrow-leaf soybean and rice), plus water, roads and houses, and mixed weeds.

| Class | Name | Samples |
|---|---|---|
| C1 | Corn | 34,511 |
| C2 | Cotton | 8,374 |
| C3 | Sesame | 3,031 |
| C4 | Broad-leaf soybean | 63,212 |
| C5 | Narrow-leaf soybean | 4,151 |
| C6 | Rice | 11,854 |
| C7 | Water | 67,056 |
| C8 | Roads and houses | 7,124 |
| C9 | Mixed weed | 5,229 |

## WHU-Hi-HanChuan

HanChuan was flown over Hanchuan on 17 June 2016, from 17:57 to 18:46, in clear weather at about 30°C and 70% humidity. The platform was a Leica Aibot X6 UAV V1 with a 17 mm lens at 250 m altitude. The image is 1217 × 303 pixels with 274 bands from 400 to 1000 nm, at about 0.109 m resolution.

The area sits on the edge between town and countryside, so it mixes buildings, water and cultivated land. Seven crops are present: strawberry, cowpea, soybean, sorghum, water spinach, watermelon and greens. One thing to keep in mind is that the flight took place in the late afternoon, when the sun was low, so a good part of the image is covered in shadow. That makes classification harder.

| Class | Name | Samples | Class | Name | Samples |
|---|---|---|---|---|---|
| C1 | Strawberry | 44,735 | C9 | Grass | 9,469 |
| C2 | Cowpea | 22,753 | C10 | Red roof | 10,516 |
| C3 | Soybean | 10,287 | C11 | Gray roof | 16,911 |
| C4 | Sorghum | 5,353 | C12 | Plastic | 3,679 |
| C5 | Water spinach | 1,200 | C13 | Bare soil | 9,116 |
| C6 | Watermelon | 4,533 | C14 | Road | 18,560 |
| C7 | Greens | 5,903 | C15 | Bright object | 1,136 |
| C8 | Trees | 17,978 | C16 | Water | 75,401 |

## WHU-Hi-HongHu

HongHu covers an area near Honghu City and was collected on 20 November 2017, between 16:23 and 17:37. It was a cloudy day, about 8°C with 55% humidity. The DJI Matrice 600 Pro flew at just 100 m with a 17 mm lens, which produces the finest detail of the three: a 940 × 475 image with 270 bands and about 0.043 m per pixel.

This is the most demanding of the three scenes. It has many crop classes, and some of them are different varieties of the same crop, such as Chinese cabbage versus cabbage, or Brassica chinensis versus small Brassica chinensis. Telling those apart takes more than a basic classifier.

| Class | Name | Samples | Class | Name | Samples |
|---|---|---|---|---|---|
| C1 | Red roof | 14,041 | C12 | Brassica chinensis | 8,954 |
| C2 | Road | 3,512 | C13 | Small Brassica chinensis | 22,507 |
| C3 | Bare soil | 21,821 | C14 | Lactuca sativa | 7,356 |
| C4 | Cotton | 163,285 | C15 | Celtuce | 1,002 |
| C5 | Cotton firewood | 6,218 | C16 | Film covered lettuce | 7,262 |
| C6 | Rape | 44,557 | C17 | Romaine lettuce | 3,010 |
| C7 | Chinese cabbage | 24,103 | C18 | Carrot | 3,217 |
| C8 | Pakchoi | 4,054 | C19 | White radish | 8,712 |
| C9 | Cabbage | 10,819 | C20 | Garlic sprout | 3,486 |
| C10 | Tuber mustard | 12,394 | C21 | Broad bean | 1,328 |
| C11 | Brassica parachinensis | 11,015 | C22 | Tree | 4,040 |

## Credits

The datasets were collected and shared by the RSIDEA research group, Wuhan University. If you use them in your own work, please cite the original paper published in *Remote Sensing of Environment*.

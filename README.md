# Circle to Search on LineageOS

## About

This module adds base support files from [MindTheGapps](https://github.com/MindTheGapps/vendor_gapps) to enforce Circle to Search integration availability introduced in LineageOS 22.2, bringing this feature to setups with microG or minimal GApps packages.

Contains:
* system resource overlay that selects Google app as the Contextual Search provider;
* [sysconfig file](./sysconfig-cts.xml) declaring `com.google.android.feature.CONTEXTUAL_SEARCH`.

## Installation

1. Flash the module and reboot;
2. If you haven't already, install or update the Google app;
3. Invoke Circle to Search by long-pressing the navigation bar. If it's not working, check if Circle to Search is enabled in Settings -> System -> Gestures -> Navigation mode. That's it.

## Build the overlay

Requires Python 3.11+, Java and zipalign. Other Android build tools are downloaded automatically.

```sh
python3 build.py
```

This builds and signs `overlay/`, then writes the APK to `output/CtsOverlay.apk`.

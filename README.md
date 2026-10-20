# Circle to Search on LineageOS

## About

This module adds base support files from [MindTheGapps](https://github.com/MindTheGapps/vendor_gapps) to enforce Circle to Search integration availability introduced in LineageOS 22.2, bringing this feature to setups with microG or minimal GApps packages.

Contains:
* system resource overlay that selects Google app as the Contextual Search provider;
* [sysconfig file](./sysconfig-cts.xml) declaring `com.google.android.feature.CONTEXTUAL_SEARCH`.

## Installation

1. Download the module from [Releases](https://github.com/reddxae/cts-on-lineage/releases/latest), flash it, and reboot;
2. If you haven't already, install or update the Google app;
3. Invoke Circle to Search by long-pressing the navigation bar. If it's not working, check if Circle to Search is enabled in Settings -> System -> Gestures -> Navigation mode. That's it.

## Build the overlay

Requires Python 3.11+, Java and zipalign. Other Android build tools are downloaded automatically.

Run:

```sh
python3 build.py
```

This builds a signed APK in `output/`.

The default signing key is public. To use your keystore, run `python3 build.py --ks /path/to/your.keystore --ks-key-alias ALIAS_NAME`; passwords are prompted.

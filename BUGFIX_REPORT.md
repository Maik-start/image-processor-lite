# 🐛 BUGFIX REPORT - Module Initialization Issue

**Date:** 29 janvier 2026  
**Commit:** `646a407`  
**Branch:** `develop`  
**Status:** ✅ FIXED

---

## Issue Summary

The package was not detecting text in real images even though the configuration was set correctly. The detection always returned empty results (0 regions) instead of the expected 20+ regions.

### Before Fix
```python
processor = ImageProcessor()
processor.config.enable_module('text_detection', True)
processor.config.set_module_options('text_detection', {...})
regions = processor.detect_text(image)
# Result: regions = [] (empty) ❌
```

### After Fix
```python
processor = ImageProcessor()
processor.config.enable_module('text_detection', True)
processor.config.set_module_options('text_detection', {...})
regions = processor.detect_text(image)
# Result: regions = [23 TextRegion objects] ✅
```

---

## Root Cause Analysis

### The Problem

1. **Module Configuration Defaults:** All modules were disabled by default in `ImageProcessorConfig`:
   ```python
   'text_detection': ModuleConfig(enabled=False, options={...})
   ```

2. **Initialization Timing:** `ImageProcessor.__init__()` called `_init_modules()` immediately:
   ```python
   def __init__(self, ...):
       self.config = ImageProcessorConfig(config_file)
       self._init_modules()  # Called HERE
   ```

3. **Early Module Creation:** Since modules were disabled at init time, they were never created:
   ```python
   # In _init_modules():
   if self.config.is_module_enabled('text_detection'):  # False!
       self.text_detector = TextDetector(...)  # Never executed
   else:
       self.text_detector = None  # Set to None
   ```

4. **Enable Module Too Late:** Calling `enable_module()` after init didn't help:
   ```python
   processor.config.enable_module('text_detection', True)
   # But self.text_detector was already None!
   ```

5. **Broken Detection:** When detect_text() was called, the detector was `None`:
   ```python
   def detect_text(self, ...):
       if not self.config.is_module_enabled('text_detection') or self.text_detector is None:
           return None  # Always here because text_detector is None
   ```

### Why Previous Versions Worked

In previous versions, modules were probably initialized at startup or with `enabled=True` by default, so the detector was created early and available when needed.

---

## Solution Implemented

### Lazy Module Initialization

Instead of creating modules once at `__init__()`, create them on first use with `_ensure_*()` methods:

```python
def _ensure_text_detector(self) -> bool:
    """Creates text_detector if needed and enabled."""
    if not self.config.is_module_enabled('text_detection'):
        return False
    if self._modules_created['text_detection'] and self.text_detector is not None:
        return True
    try:
        # Create detector on first use
        options = self.config.get_module_options('text_detection')
        self.text_detector = TextDetector(...)
        self._modules_created['text_detection'] = True
        return True
    except Exception as e:
        self.text_detector = None
        return False
```

### Updated Methods

All public methods now use `_ensure_*()` instead of checking config:

```python
# Before
def detect_text(self, image, ...):
    if not self.config.is_module_enabled('text_detection') or self.text_detector is None:
        return None
    return self.text_detector.detect(image, ...)

# After
def detect_text(self, image, ...):
    if not self._ensure_text_detector():
        return None
    return self.text_detector.detect(image, ...)
```

---

## Changes Made

**File:** `imgprocessor/__init__.py`

### Changes
- Removed eager module initialization from `__init__()`
- Added `_modules_created` tracking dict
- Implemented `_ensure_text_detector()`, `_ensure_shape_detector()`, `_ensure_distance_measurer()`, `_ensure_visual_analyzer()`
- Updated all public methods to use `_ensure_*()` methods
- Kept `_init_modules()` for backward compatibility

### Impact
- ✅ 100% backward compatible - existing code works unchanged
- ✅ Dynamic module enable/disable now works correctly
- ✅ Lazy loading reduces startup time even more
- ✅ Fixes the real-world image detection issue

---

## Test Results

### Text Detection Test
```
Image loaded: (270, 480, 3)
ImageProcessor created
text_detector before enable: None
Module text_detection enabled
Regions detected: 23 ✅
  - Text: partir des pixels..., Confidence: 0.90
  - Text: espace latent (embedding)..., Confidence: 0.70
  - Text: pour..., Confidence: 1.00
```

### Performance Impact
- No additional overhead
- Modules created once and cached in `_modules_created`
- Subsequent calls return immediately

---

## Backward Compatibility

✅ **100% Backward Compatible**

This fix maintains full backward compatibility:
1. Existing code that enables modules at init still works
2. Code using default settings is unaffected
3. API signatures unchanged
4. Return values unchanged

---

## Files Modified

- ✅ `imgprocessor/__init__.py`

---

## Next Steps

- ✅ Run full test suite (all tests pass)
- ✅ Test with real images (confirmed working)
- ✅ Push to GitHub

---

## Related Issues

- Related to lazy-loading optimizations in recent commits
- Complements OCR lazy-loading in `text_detection/detector.py`
- Part of performance optimization initiative (v1.0.2)

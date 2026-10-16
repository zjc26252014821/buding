// The payload is the patched MangoPanelBackgroundPlayback.dylib in layout/.
// This empty bundle target only lets Theos perform roothide packaging/signing.
int mango_thermal_fix_dummy(void) { return 0; }

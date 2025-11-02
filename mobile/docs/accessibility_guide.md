# Accessibility Guide

## Current Implementation

### Semantic Labels
- Use `Semantics` widget for screen readers
- Label all interactive elements
- Provide meaningful descriptions

### Color Contrast
- Text meets WCAG AA standards (4.5:1 for normal text)
- Brand colors tested for contrast
- Use of color alone avoided for information

### Tap Targets
- Minimum 48x48dp tap targets
- Adequate spacing between interactive elements
- Large text option support

## Best Practices

### 1. Semantic Labels
```dart
Semantics(
  label: 'Add product to cart',
  button: true,
  child: IconButton(...),
)
```

### 2. Screen Reader Support
- Provide text alternatives for icons
- Announce dynamic content changes
- Structure content logically

### 3. Keyboard Navigation
- Support keyboard navigation (web)
- Logical focus order
- Visible focus indicators

### 4. Text Scaling
- Support dynamic type sizing
- Test with system text scale settings
- Avoid fixed font sizes where possible

### 5. Color Independence
- Don't rely solely on color to convey information
- Use icons or text labels
- Ensure information is accessible in grayscale

## Testing

- Enable TalkBack on Android
- Enable VoiceOver on iOS
- Test with text scaling at maximum
- Test in grayscale mode
- Use accessibility scanner tools


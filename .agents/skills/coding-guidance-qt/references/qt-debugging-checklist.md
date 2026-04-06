# Qt Debugging Checklist

Open this reference when the task is primarily diagnosis rather than ordinary
implementation.

## Use when

- the failure class is still unclear and you need to categorize before editing
- the bug looks like ownership, signal/slot, layout, thread-affinity, or style
  breakage
- the change is mostly diagnosis rather than feature or refactor work

## Fast categorization

Classify the symptom before changing code:

- invisible widget
- zero-size widget or collapsed layout
- deleted-object access
- cross-thread QObject misuse
- pre-`QApplication` GUI object construction
- frozen event loop / blocked GUI thread
- signal connected but never fires
- style or QSS mismatch

## High-value checks

### Invisible or collapsed widget

- check `isVisible()`, `isHidden()`, and actual size
- verify parent visibility for child widgets
- verify a real layout is attached
- check `QSizePolicy`, stretch, minimum size, margins, and accidental
  `setFixedSize(0, 0)`

### Deleted-object or lifecycle bug

- check whether the object is owned by a parent that is already gone
- check `deleteLater()` timing and queued callbacks
- prefer `QPointer` for observing objects with unstable lifetime
- in C++, use ASan before guessing

### Thread-affinity bug

- look for cross-thread parent/child creation
- verify where the receiver lives, not only where the signal was emitted
- make queued delivery explicit if the hop matters

### Signal path bug

- verify sender lifetime
- verify exact signal/slot signature compatibility
- verify `Q_OBJECT` is present and moc reran after the last change

### Frozen UI

- find the blocking call on the GUI thread
- move I/O or heavy work off-thread
- treat `processEvents()` as diagnosis only, not the final fix

### Style or QSS bug

- inspect the effective stylesheet
- use local `unpolish()` / `polish()` and `update()` to confirm rule
  application before changing rendering logic

## Review hotspots

- code changes made before the failure class was identified
- `processEvents()` used as a production fix instead of diagnosis
- guessed lifecycle or thread explanations without checking object ownership or
  affinity
- layout or style fixes applied without verifying the actual geometry or active
  stylesheet state

## Useful C++ diagnostics

```cpp
qDebug() << "size" << widget->size();
qDebug() << "class" << widget->metaObject()->className();
qWarning() << "unexpected state" << state;
```

## Validation

- the root failure class is identified
- the fix removes the cause instead of hiding the symptom
- the relevant test or smoke path reproduces the fix deterministically

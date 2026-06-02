# Snowman widget overflow on catalog page

Screenshot report:
The floating AI Snowman chat widget shows a large white QR-like rectangle protruding from the circular avatar button.

Expected:
The avatar should stay contained inside a clean circular button on mobile and desktop.

Likely affected files:
- components/ai-snowman/SnowmanAvatar.tsx
- components/ai-snowman/SnowmanAssistant.tsx
- components/SplineRobotOnlyScene.tsx

Verification:
- Run the project source-contract check.
- Run typecheck/build.
- Browser-check the exact page from the screenshot.
- Confirm overflow/clipping and z-index are correct.

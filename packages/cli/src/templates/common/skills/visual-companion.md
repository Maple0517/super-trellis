# Trellis Visual Companion

Use this skill to make visual tradeoffs inspectable. It is optional, but the decision to use or skip it is mandatory for visual frontend work.

## Runnable Fallback

1. Create `.trellis/workspace/visual-companion/index.html` containing current options, screenshots, or rough mockups.
2. Start a local static server from `.trellis/workspace/visual-companion`:

   ```bash
   cd .trellis/workspace/visual-companion
   python3 -m http.server 8765
   ```

3. Give the user `http://localhost:8765/` and ask for visual feedback.
4. Capture accepted visual decisions into `prd.md`, `design.md`, or task notes.
5. Stop the server when done.

If local browser/server use is unavailable, create the HTML artifact anyway and report the file path as the fallback.

## Minimal HTML Template

```html
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Trellis Visual Companion</title>
    <style>
      body { font-family: system-ui, sans-serif; margin: 32px; background: #f7f4ef; color: #191714; }
      .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
      .card { background: white; border: 1px solid #ddd6c9; border-radius: 16px; padding: 20px; }
    </style>
  </head>
  <body>
    <h1>Visual options</h1>
    <div class="grid">
      <section class="card"><h2>Option A</h2><p>Describe or mock the visual direction.</p></section>
      <section class="card"><h2>Option B</h2><p>Describe or mock the visual direction.</p></section>
    </div>
  </body>
</html>
```

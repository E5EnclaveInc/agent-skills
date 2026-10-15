---
name: creative-production
description: "Produce finished creative assets from reference images: a group portrait with a mandatory face-quality pass, video animation of the verified still, and square icon artwork. Use when a user wants character art, campaign creatives, logos, or animated clips from their own reference images — never for the agent platform's own avatar/self-image pipeline."
license: MIT
metadata:
  version: 1.0.0
---

# Creative Production

## Purpose

Turn the user's reference images into a finished creative suite for their own
pursuits: one group portrait, a face-quality pass, an animation, and square
icon artwork. This is the user-brand twin of the agent's avatar pipeline —
same craft, but the output belongs to the user's brand, never to the agent's
self-image.

## Workflow

1. **Collect references.** User-supplied images; order matters — lead first,
   then the rest in the order the user gave.
2. **Group portrait** with your image-generation tool. One call, one output
   image. Prompt = the ordered references plus a short text entry naming the
   group, in words close to the user's request. Keep the request wording near
   verbatim apart from describing a single output image, and let the images
   carry the likeness.
3. **Face-quality pass (canonical, never skipped).** Resume the portrait
   generation (session-resume, text only) with: "Quality pass on their faces:
   make every face as beautiful as the reference examples — refined, luminous,
   golden-ratio features, expressive detailed eyes. Finalize the picture,
   with the composition optimized for animation: crisp detail, clean
   separation between figures, even cinematic lighting, no blur." Face
   quality is a standing gate — never call a portrait final without this
   pass.
4. **Verify the still firsthand** by opening the returned file before
   presenting it. A successful generation response proves a file exists, not
   how it looks.
5. **Animate** the verified still with your video-generation tool and a
   short motion prompt drawn from the request (e.g. "gentle cinematic
   motion — hair and fabric drifting, light shimmering, petals floating").
   Verify firsthand: extract one frame (e.g.
   `ffmpeg -ss 1 -i <mp4> -frames:v 1 /tmp/check.png`) and view it before
   presenting.
6. **Icon artwork** with your icon/square-artwork tool when the user asks
   for a logo, app icon, or product mark. Describe only the subject and
   mood — the tool's square-icon art direction applies automatically — and
   note the surface where the icon will live (app, web, podcast, generic).
7. **Present** each finished asset on its own line, stating plainly which
   requested pieces are included. Report a generation or verification
   failure as a failure rather than presenting an unchecked file as
   finished.

## Output contract

- Final still: face-quality-passed, animation-ready.
- Video: animated version of the verified still, frame-verified before
  delivery.
- Icon: square artwork, only when requested.

## Operating rules

- Image generation: copy the user's request near verbatim apart from
  describing a single output image; when resuming a generation, include
  only newly introduced image references.
- Video generation: keep the motion prompt short and drawn from the
  request; the verified still is the anchor frame.
- Icon generation: describe subject and mood, never restate the icon
  styling; state the intended surface honestly.
- **Never use the agent platform's own avatar / self-image pipeline for
  user brand work.** That pipeline makes the agent's self-image and is
  off-limits here. If the user asks for "an avatar" for themselves, build
  a user character avatar candidate with the image/icon tools above — only
  when explicitly asked — and say plainly that it is not the
  avatar-pipeline path.
- Verify stills and video frames firsthand before presenting.
- Adult creative direction from the user is passed through as-is; the
  generation tools own policy decisions.

## Alternatives for better results

- Ask for stronger reference images when likeness matters more than speed —
  the portrait can only carry the detail the references supply.
- Split a crowded crew into a smaller lead group when faces lose detail,
  then build the wider portrait from the verified lead result.

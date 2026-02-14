# dims - VSCode Extension Project Plan

## Overview
**Product:** VSCode extension that displays array/tensor shapes directly in the debug variables view  
**Target Users:** Python developers working with NumPy, PyTorch, TensorFlow, pandas  
**Business Model:** OSS (MIT) + Ko-fi donations  
**Timeline:** Ship in 3 days

---

## Core Value Proposition

**Problem:** Developers constantly switch between debug view and console to check `.shape` on arrays/tensors  
**Solution:** Display shape inline: `{[2, 3]}, tensor([[2, 3]...` instead of `tensor([[2, 3]...`

---

## Technical Foundation

### Current Implementation
- Modified debugpy extension file: `pydevd_plugin_pytorch_tensor_str.py`
- Uses `StrPresentationProvider` API
- ~15 lines of code
- Detects `collections.abc.Sized` objects with `.shape` attribute

### Migration Required
**From:** Manual file edit in vendored debugpy code  
**To:** Standalone VSCode extension

**Key Technical Tasks:**
1. VSCode extension boilerplate (`yo code`)
2. Integration with debugpy visualization API
3. Configuration options (enable/disable, format customization)
4. Testing across Python environments

---

## Shipping Plan

### Phase 1: Package (Day 1, ~3 hours) ✅ COMPLETED
- [x] Set up VSCode extension structure
- [x] Port plugin code to extension format
- [x] Create proper Python plugin directory structure
- [x] Add TypeScript configuration and compile extension
- [x] Write README with before/after visuals
- [x] Add MIT LICENSE
- [x] Create test scripts for manual testing
- [x] Fix placeholder URLs and remove missing icon reference

### Phase 2: Polish (Day 2, ~2 hours)
- [ ] Record 10-second demo GIF
- [ ] Enhance README (problem â†’ solution â†’ install)
- [ ] Create GitHub repository
- [ ] Tag v1.0.0 release

### Phase 3: Publish (Day 2, ~1 hour)
- [ ] Create VSCode Marketplace publisher account
- [ ] Package extension (`vsce package`)
- [ ] Publish to marketplace (`vsce publish`)
- [ ] Verify live listing

### Phase 4: Launch (Day 3, ~2 hours)
- [ ] r/Python: "See array shapes instantly while debugging [Show]"
- [ ] r/MachineLearning (if targeting ML devs)
- [ ] Hacker News Show HN
- [ ] Optional: Twitter/LinkedIn with demo GIF

### Phase 5: Iterate (Ongoing)
- [ ] Monitor GitHub issues
- [ ] Personal response to first 5 users
- [ ] Ship v1.1 with user feedback (within 2 weeks)

---

## Marketing Strategy

### âœ… DO
- Lead with pain point: "Tired of typing .shape in the console?"
- Show before/after comparison
- Simple, technical demo GIF
- Focus on time savings and reduced friction
- Professional, clean presentation

### âŒ DON'T
- No meme marketing (Rick & Morty, etc.)
- No hype or exaggeration
- No "revolutionary" claims
- No cartoon imagery or pop culture references

### Launch Copy Template
```
Title: See array shapes instantly while debugging [Show]

Before: Constantly switching to console to check .shape
After: Shapes display inline in debug view

[GIF showing the feature]

Free VSCode extension: [link]
GitHub: [link]
```

---

## Monetization Reality Check

### Ko-fi Donations
**Expected:** $20-200/year total  
**Conversion:** ~0.1-0.2% of users donate  
**Real value:** 
- Superfan identification
- Feature request signals
- Market validation for next tools

**Setup:**
- Ko-fi or GitHub Sponsors link in README
- One line: "Find this useful? [Buy me a coffee â˜•]"
- No aggressive asks

### Long-term Play
This extension is **reputation capital**, not revenue:
- Portfolio piece
- Credibility builder
- First step in "ML dev tooling" positioning
- Practice shipping quickly

---

## Success Metrics

### Week 1
- [ ] 100 installs
- [ ] 3+ GitHub stars
- [ ] 1-2 pieces of user feedback

### Month 1
- [ ] 500 installs
- [ ] 10+ GitHub stars
- [ ] First donation (maybe)

### Month 3
- [ ] 1,000+ installs
- [ ] Clear signal on next feature to build
- [ ] Decide: keep as solo tool or expand to suite

---

## Risk Mitigation

### Competition
**Risk:** Someone forks and publishes first  
**Mitigation:** Ship fast (this week), own the name "dims"

### Marketplace Rejection
**Risk:** Extension doesn't meet VSCode guidelines  
**Mitigation:** Follow official extension tutorial, test thoroughly

### User Adoption
**Risk:** Nobody cares  
**Mitigation:** This is learning exercise. Even 50 users = success.

---

## Technical Risks & Solutions

### Debugpy Updates Breaking Integration
**Risk:** API changes in debugpy  
**Solution:** Pin to stable API, monitor debugpy releases

### Performance with Large Arrays
**Risk:** Computing shape on huge tensors slows debugger  
**Solution:** Add configuration to disable for objects >X size

### Cross-platform Issues
**Risk:** Works on Linux, breaks on Windows/Mac  
**Solution:** Test on all platforms before v1.0

---

## Next Steps (Right Now)

1. Check if "dims" is available on VSCode Marketplace
2. Create GitHub repo: `dims-vscode`
3. Run `yo code` to scaffold extension
4. Port existing code
5. Test locally

**Decision point:** If "dims" is taken, backup name is "debugshapes"

---

## Resources Needed

- VSCode extension development docs
- debugpy plugin API documentation
- Screen recording tool for GIF
- ~8 hours of focused work
- GitHub account
- VSCode Marketplace publisher account (free)

---

## Philosophy

**Ship fast, iterate faster.**  
This isn't the million-dollar idea. It's practice for finding it.  
Perfect is the enemy of shipped.  
Learn in public, build in public, fail in public.

---

**Status:** Phase 1 Complete ✅ → Ready for Phase 2 (Polish)
**Completed:** Extension structure, TypeScript compilation, Python plugin, tests, LICENSE
**Next action:** Record demo GIF, enhance README, create polished GitHub repo
**Current branch:** claude/review-project-phase-ZYaNn
**Target ship date:** Monday
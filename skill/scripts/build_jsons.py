#!/usr/bin/env python3
"""Assemble the three AI Use Case JSON files from a collected answers.json.

Usage:
  python3 build_jsons.py --answers answers.json --out-dir ./out --basename ms_plan_designer

Emits <basename>.template.json, <basename>.layout.json, <basename>.design_system.json.
Derives the header/timeline gradients from the primary brand color and validates enums.
"""
import argparse, json, os, sys, re

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

def fail(msg):
    print(f"ERROR: {msg}", file=sys.stderr); sys.exit(1)

def shade(hexcolor, factor):
    """OOXML 'shade': multiply each RGB channel toward black by factor (0..1)."""
    h = hexcolor.lstrip("#")
    r,g,b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    f = lambda c: max(0, min(255, round(c*factor)))
    return "#%02X%02X%02X" % (f(r), f(g), f(b))

def lum(hexcolor, lummod, lumoff=0.0):
    """Approximate OOXML lumMod/lumOff."""
    h = hexcolor.lstrip("#")
    r,g,b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    f = lambda c: max(0, min(255, round(c*lummod + 255*lumoff)))
    return "#%02X%02X%02X" % (f(r), f(g), f(b))

def validate(ans):
    rate3 = {"High","Medium","Low"}
    risk3 = {"High","Med","Low"}
    if ans["businessValue"]["rating"] not in rate3 | {"TBD"}:
        fail(f"businessValue.rating must be High/Medium/Low")
    if ans["feasibility"]["overall"] not in rate3 | {"TBD"}: fail("feasibility.overall invalid")
    for fct in ans["feasibility"]["factors"]:
        if fct["rating"] not in rate3 | {"TBD"}: fail(f"feasibility factor '{fct['factor']}' rating invalid")
    if ans["risks"]["overall"] not in risk3 | {"TBD"}: fail("risks.overall must be High/Med/Low")
    for fct in ans["risks"]["factors"]:
        if fct["rating"] not in risk3 | {"TBD"}: fail(f"risk factor '{fct['factor']}' rating must be High/Med/Low")
    if ans["solutionPath"]["selected"] not in {"Buy","Build","Extend"}:
        fail("solutionPath.selected must be Buy/Build/Extend")
    for m in (ans["timeline"]["startMonth"], ans["timeline"]["endMonth"]):
        if m not in MONTHS: fail(f"month '{m}' not in Jan..Dec")
    px = ans.get("design",{}).get("primaryHex","#2576B7")
    if not re.fullmatch(r"#?[0-9A-Fa-f]{6}", px): fail("design.primaryHex must be 6-digit hex")

def build_template(ans):
    sel = ans["solutionPath"]["selected"]
    opts = []
    for v in ["Buy","Build","Extend"]:
        label = ans["solutionPath"].get("selectedLabel", v) if v==sel else v
        opts.append({"value": v, "displayLabel": label, "selected": v==sel})
    si = MONTHS.index(ans["timeline"]["startMonth"]); ei = MONTHS.index(ans["timeline"]["endMonth"])
    sel_months = {m: (si <= i <= ei) for i,m in enumerate(MONTHS)}
    return {
        "templateName": "AI Use Case One-Pager",
        "templateVersion": "1.0",
        "fields": {
            "header": {
                "title": {"shapeName":"Title 1","value": ans["identity"]["title"]},
                "strategicStatement": {"shapeName":"Title 1","value": ans["identity"]["strategicStatement"]},
                "useCaseTag": {"value":"AI USE CASE","editable": False},
                "useCaseName": {"value": ans["identity"]["useCaseName"]}
            },
            "initiativeDescription": {
                "subFields": {
                    "overview": {"value": ans["initiative"]["overview"]},
                    "capabilities": {"items": ans["initiative"]["capabilities"]},
                    "scopeOfImplementation": {"heading":"Scope of Implementation:","items": ans["initiative"]["scope"]}
                }
            },
            "solutionPath": {"type":"singleSelect","allowedValues":["Buy","Build","Extend"],"options": opts},
            "businessValue": {
                "rating": {"allowedValues":["High","Medium","Low"],"value": ans["businessValue"]["rating"]},
                "description": {"value": ans["businessValue"]["description"]}
            },
            "feasibility": {
                "overallRating": {"allowedValues":["High","Medium","Low"],"value": ans["feasibility"]["overall"]},
                "factors": {"factorAllowedValues":["High","Medium","Low"],"items": ans["feasibility"]["factors"]}
            },
            "risks": {
                "overallRating": {"allowedValues":["High","Med","Low"],"value": ans["risks"]["overall"]},
                "factors": {"factorAllowedValues":["High","Med","Low"],"items": ans["risks"]["factors"]}
            },
            "otherExpectedBenefits": {
                "subFields": {"successMetrics": {"heading": ans["otherBenefits"]["heading"],"items": ans["otherBenefits"]["items"]}}
            },
            "complexityDependencies": {
                "subFields": {"dependency": {"value": ans["complexity"]["dependency"]},
                              "complexity": {"value": ans["complexity"]["complexity"]}}
            },
            "projectTeam": {"roles": {
                "businessSponsor": {"label":"Business Sponsor","value": ans["team"]["businessSponsor"]},
                "itSponsor": {"label":"IT Sponsor","value": ans["team"]["itSponsor"]},
                "projectManager": {"label":"PM","value": ans["team"]["projectManager"]},
                "subjectMatterExpert": {"label":"SME","value": ans["team"]["sme"]}
            }},
            "desiredProjectTimelineRange": {
                "summaryBadge": {"value": ans["timeline"]["badge"]},
                "timeline": {"year": {"value": ans["timeline"]["year"]},
                             "months": MONTHS,
                             "selectedMonths": {"value": sel_months}}
            }
        }
    }

def build_design(ans):
    d = ans.get("design", {})
    base = os.path.join(ASSETS, "design_system.default.json")
    ds = json.load(open(base))
    if not d.get("reskin"): 
        return ds
    p = "#" + d.get("primaryHex","#2576B7").lstrip("#").upper()
    ds["version"] = "1.0-custom"
    ds["derivedFrom"] = f"ai-use-case-builder re-skin from primary {p}"
    ds["colorPalette"]["theme"]["accent1_primaryBlue"] = p
    ds["colorPalette"]["semantic"]["primary"] = p
    ds["colorPalette"]["semantic"]["cardBorder"] = p
    ds["colorPalette"]["semantic"]["subtitleText"] = p
    ds["colorPalette"]["semantic"]["ratingBadgeText"] = p
    # regenerate gradients
    ds["gradients"]["headerBar"]["baseColor"] = p
    s0,s1,s2 = shade(p,0.30), shade(p,0.675), shade(p,1.0)
    ds["gradients"]["headerBar"]["stops"] = [
        {"pos":0.0,"shade":0.30,"approxHex":s0},
        {"pos":0.50,"shade":0.675,"approxHex":s1},
        {"pos":1.0,"shade":1.0,"approxHex":s2}]
    ds["gradients"]["headerBar"]["cssApprox"] = f"linear-gradient(45deg, {s0} 0%, {s1} 50%, {s2} 100%)"
    ds["gradients"]["aiUseCaseHeroBox"]["baseColor"] = p
    ds["gradients"]["aiUseCaseHeroBox"]["cssApprox"] = f"linear-gradient(160deg, {shade(p,0.30)} 0%, {p} 70%, {lum(p,1.0,0.18)} 100%)"
    t0,t1 = lum(p,0.75), lum(p,0.60,0.40)
    ds["gradients"]["timelineProgressBar"]["baseColor"] = p
    ds["gradients"]["timelineProgressBar"]["stops"] = [
        {"pos":0.0,"lumMod":0.75,"approxHex":t0},
        {"pos":0.50,"lumMod":0.60,"lumOff":0.40,"approxHex":t1},
        {"pos":1.0,"lumMod":0.60,"lumOff":0.40,"approxHex":t1}]
    ds["gradients"]["timelineProgressBar"]["cssApprox"] = f"linear-gradient(90deg, {t0} 0%, {t1} 50%, {t1} 100%)"
    if d.get("headerFont"): ds["typography"]["fontFamilies"]["sectionHeader"] = d["headerFont"]
    if d.get("bodyFont"): ds["typography"]["fontFamilies"]["body"] = d["bodyFont"]
    if d.get("ratingColors"): ds["colorPalette"]["ratingColors"].update(d["ratingColors"])
    return ds

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--answers", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--basename", required=True)
    a = ap.parse_args()
    ans = json.load(open(a.answers))
    validate(ans)
    os.makedirs(a.out_dir, exist_ok=True)
    tpl = build_template(ans)
    layout = json.load(open(os.path.join(ASSETS, "layout.json")))
    ds = build_design(ans)
    out = lambda suf, obj: json.dump(obj, open(os.path.join(a.out_dir, f"{a.basename}.{suf}.json"),"w"), indent=2)
    out("template", tpl); out("layout", layout); out("design_system", ds)
    print(f"Wrote {a.basename}.template.json, {a.basename}.layout.json, {a.basename}.design_system.json to {a.out_dir}")

if __name__ == "__main__":
    main()

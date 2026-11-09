#!/usr/bin/env python3
"""
Mobile Test Automation Framework Audit Scanner.

Analyzes a mobile automation codebase (WDIO, Appium, Cucumber, TypeScript) against
enterprise architectural rules, detecting anti-patterns, flakiness hazards,
security issues, and locator fragility.
"""

import os
import re
import sys
import json
from pathlib import Path
from typing import List, Dict, Any

class MobileFrameworkAuditor:
    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir).resolve()
        self.findings: List[Dict[str, Any]] = []

    def log_finding(self, rule_id: str, severity: str, file_path: Path, line_num: int, title: str, recommendation: str, snippet: str = ""):
        try:
            rel_path = file_path.relative_to(self.target_dir)
        except ValueError:
            rel_path = file_path
        self.findings.append({
            "rule_id": rule_id,
            "severity": severity,
            "file": str(rel_path),
            "line": line_num,
            "title": title,
            "recommendation": recommendation,
            "snippet": snippet.strip()
        })

    def audit_file_content(self, file_path: Path):
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except Exception:
            return

        for idx, line in enumerate(lines, start=1):
            # 1. Hardcoded sleeps / pauses
            if re.search(r'\b(browser\.pause|sleep\s*\(|Thread\.sleep)\b', line) and not line.strip().startswith("//"):
                self.log_finding(
                    rule_id="MOB-001",
                    severity="HIGH",
                    file_path=file_path,
                    line_num=idx,
                    title="Hardcoded sleep / pause detected",
                    recommendation="Replace hardcoded pause with explicit condition-based wait using WaitUtils.",
                    snippet=line
                )

            # 2. Fragile generic class selectors without landmark scoping
            if re.search(r'className\s*\(\s*["\'](android\.widget\.(EditText|Button|TextView)|XCUIElementType(TextField|Button))\b', line):
                self.log_finding(
                    rule_id="MOB-002",
                    severity="MEDIUM",
                    file_path=file_path,
                    line_num=idx,
                    title="Fragile generic class selector without scoping",
                    recommendation="Prioritize accessibilityId or scoped semantic resource IDs over bare class selectors.",
                    snippet=line
                )

            # 3. Brittle positional / index XPaths
            if re.search(r'\(\s*//(android|XCUIElementType)[^)]+\)\[\s*\d+\s*\]', line):
                self.log_finding(
                    rule_id="MOB-003",
                    severity="HIGH",
                    file_path=file_path,
                    line_num=idx,
                    title="Brittle positional index XPath selector",
                    recommendation="Avoid index-based XPaths (e.g., (//android.widget.EditText)[1]). Use unique accessibilityId or relative landmark scoping.",
                    snippet=line
                )

            # 4. Direct browser.waitUntil in Screen Classes bypassing Utility layer
            if "screens" in str(file_path).lower() and re.search(r'\bbrowser\.waitUntil\b', line):
                self.log_finding(
                    rule_id="MOB-004",
                    severity="LOW",
                    file_path=file_path,
                    line_num=idx,
                    title="Screen object bypassing WaitUtils layer",
                    recommendation="Route element synchronization through BaseScreen waits (WaitUtils) for consistent timeout policy.",
                    snippet=line
                )

            # 5. Potential hardcoded credentials / PIN / OTP in test specs
            if ("spec" in str(file_path).lower() or "test" in str(file_path).lower()) and not line.strip().startswith("//"):
                if re.search(r'\b(pin|password|otp|secret)\s*[:=]\s*["\'][0-9a-zA-Z]{3,}["\']', line, re.IGNORECASE):
                    self.log_finding(
                        rule_id="MOB-005",
                        severity="HIGH",
                        file_path=file_path,
                        line_num=idx,
                        title="Potential hardcoded credential / secret in test file",
                        recommendation="Externalize credentials and OTP into TestDataService or environment variables.",
                        snippet=line
                    )

            # 6. Duplicated Gesture Scroll search overlapping ScrollUtils
            if "gestureutils" in str(file_path).lower() and re.search(r'\b(scrollToText|scrollIntoView)\b', line):
                self.log_finding(
                    rule_id="MOB-006",
                    severity="MEDIUM",
                    file_path=file_path,
                    line_num=idx,
                    title="Scroll workflow embedded in GestureUtils",
                    recommendation="GestureUtils should contain only gesture primitives. Move high-level scroll searches to ScrollUtils.",
                    snippet=line
                )

    def audit_tsconfig(self):
        tsconfig_path = self.target_dir / "tsconfig.json"
        if tsconfig_path.exists():
            try:
                with open(tsconfig_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if '"strict": false' in content or "'strict': false" in content:
                        self.log_finding(
                            rule_id="MOB-007",
                            severity="MEDIUM",
                            file_path=tsconfig_path,
                            line_num=1,
                            title="TypeScript strictness disabled",
                            recommendation="Enable strict mode in tsconfig.json to prevent runtime null pointer and type drift issues.",
                            snippet='"strict": false'
                        )
            except Exception:
                pass

    def run_audit(self) -> Dict[str, Any]:
        extensions = {".ts", ".js", ".feature"}
        for root, dirs, files in os.walk(self.target_dir):
            # Ignore node_modules, dist, build, coverage, allure-results
            dirs[:] = [d for d in dirs if d not in {"node_modules", "dist", "build", "coverage", ".git", "allure-results", "allure-report"}]
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in extensions:
                    self.audit_file_content(file_path)

        self.audit_tsconfig()

        high_count = sum(1 for f in self.findings if f["severity"] == "HIGH")
        medium_count = sum(1 for f in self.findings if f["severity"] == "MEDIUM")
        low_count = sum(1 for f in self.findings if f["severity"] == "LOW")

        return {
            "target": str(self.target_dir),
            "total_findings": len(self.findings),
            "summary": {
                "high": high_count,
                "medium": medium_count,
                "low": low_count
            },
            "findings": self.findings
        }

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    auditor = MobileFrameworkAuditor(target)
    results = auditor.run_audit()

    print("\n==================================================")
    print("      MOBILE AUTOMATION ARCHITECTURE AUDIT        ")
    print("==================================================")
    print(f"Target Directory: {results['target']}")
    print(f"Total Findings:   {results['total_findings']}")
    print(f"High Severity:    {results['summary']['high']}")
    print(f"Medium Severity:  {results['summary']['medium']}")
    print(f"Low Severity:     {results['summary']['low']}")
    print("--------------------------------------------------\n")

    if not results["findings"]:
        print("No mobile automation architectural anti-patterns found. Framework clean!")
        return 0

    for f in results["findings"]:
        print(f"[{f['severity']}] {f['rule_id']}: {f['title']}")
        print(f"  Location:       {f['file']}:{f['line']}")
        print(f"  Recommendation: {f['recommendation']}")
        if f["snippet"]:
            print(f"  Snippet:        {f['snippet']}")
        print()

    return 1 if results["summary"]["high"] > 0 else 0

if __name__ == "__main__":
    sys.exit(main())


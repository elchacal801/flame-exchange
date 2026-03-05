# Baseline: E-Commerce Payment Page Integrity

```yaml
---
id: BL-0015
title: "E-Commerce Payment Page Integrity Baseline"
category: Baseline
date: 2026-03-04
author: "FLAME Project"
tags:
  - e-skimmer
  - magecart
  - payment-page
  - script-integrity
  - csp
  - gtm
  - dom-monitoring
  - pci-dss
---
```

## Description

This baseline defines normal versus anomalous patterns for e-commerce payment page integrity, supporting detection logic for TP-0035 (Magecart E-Skimmer Data Compromise). It establishes behavioral norms for checkout page script loading, Content Security Policy violation rates, Google Tag Manager container modification frequency, DOM mutation rates on payment form elements, and external domain calls during the checkout flow. These baselines are derived from Recorded Future's 2025 Annual Payment Fraud Intelligence Report, PCI DSS 4.0 Requirement 6.4.3 implementation guidance, and client-side security monitoring vendor research (Feroot, Jscrambler, Source Defense). Organizations should calibrate these thresholds to their specific e-commerce platform, payment processor integration, and marketing technology stack.

## Normal Patterns

* **Checkout Page Script Count:** Legitimate e-commerce checkout pages load a median of **8-15 external scripts** including payment processor SDKs, analytics libraries, and marketing tags. Established stores show stable script counts with changes occurring only during scheduled deployments. An increase of **3 or more** external scripts outside a deployment window is anomalous and warrants investigation. Scripts loading from domains registered within the past **90 days** should be flagged for review regardless of whether they cause a CSP violation.

* **CSP Violation Rate:** Well-configured e-commerce sites with enforced Content Security Policies on payment pages experience CSP violations on **fewer than 0.1%** of page loads. These violations are typically caused by browser extensions, outdated cached pages, or minor configuration drift. A sustained CSP violation rate exceeding **0.3%** on payment pages for more than 1 hour, or any violation involving script execution from an unrecognized domain, is a high-priority indicator. Violation rates exceeding **1.0%** should trigger immediate investigation.

* **GTM Container Modification Frequency:** Established e-commerce stores modify Google Tag Manager containers **fewer than 2 times per week** on average. Modifications are clustered around marketing campaign launches and typically occur during business hours (9 AM - 6 PM local time). Container modifications outside business hours, creation of Custom HTML tags, or addition of tags that load external JavaScript from non-whitelisted domains are anomalous. New stores or stores undergoing active marketing campaigns may legitimately modify containers **3-5 times per week**.

* **DOM Mutation Rate on Payment Form Elements:** Legitimate payment page checkout flows should produce **zero** non-framework DOM mutations on payment form elements (card number, expiration date, CVV, billing address fields, and submit buttons) during the checkout process. All payment form DOM manipulation should originate from the authorized front-end framework (React, Angular, Vue, or the payment processor's embedded form SDK). Any mutation source outside the framework context — including injected script tags, inline event handlers, new iframe elements, or overlay div elements positioned over payment inputs — is a critical anomaly.

* **External Domain Calls During Checkout:** During the checkout flow, payment pages typically communicate with **3-7 known domains** including the payment processor (e.g., Stripe, PayPal, Adyen), analytics services (Google Analytics, Segment), and the merchant's own API endpoints. The set of contacted domains should be stable across sessions with changes only occurring during authorized deployments. Any outbound request to an unrecognized domain during checkout — particularly POST requests, WebSocket connections, or image/beacon requests with encoded URL parameters — is anomalous and should be investigated immediately.

* **Script Content Hash Stability:** Third-party script content hashes on payment pages should remain stable between authorized deployment windows. Legitimate script updates (payment processor SDK versions, analytics library updates) typically occur **fewer than once per month** per script and correlate with vendor release announcements. A hash change in any script loaded on the payment page that does not correlate with a known vendor update or an internal deployment is a potential indicator of supply chain compromise or script injection.

## Application to Detection

Detection rules for TP-0035 should layer multiple integrity signals rather than relying on any single indicator. A CSP violation alone has moderate false positive rates (browser extensions, configuration drift), but a CSP violation combined with a new script load from a recently registered domain and a DOM mutation on a payment form element creates a high-confidence composite signal for e-skimmer injection.

Threshold tuning should account for platform complexity: merchants using multiple payment methods (credit card, PayPal, Apple Pay, Google Pay) will have higher baseline script counts and more external domain calls than single-payment-method stores. Merchants with active marketing campaigns may have higher GTM modification rates. These platform-specific baselines should be established per merchant and refined over the first 30 days of monitoring.

Real-time monitoring is essential — e-skimmer infections have a median dwell time of 22 days (Recorded Future), and every hour of undetected infection represents additional compromised transactions. Detection latency should target under 1 hour from script injection to alert generation, with automated response playbooks that can isolate the payment page pending investigation.

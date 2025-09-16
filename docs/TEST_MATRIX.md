# HURL Test Infrastructure Diagram

```
HURL Advanced Test Scheme
┌─────────────────────────────────────────────────────────────────────────────┐
│                              TEST DATA SOURCES                             │
└─────────────────────────────────────────────────────────────────────────────┘

   🎭 MOCKED DATA          💾 CACHED DATA          🌐 REMOTE DATA
   ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
   │ tests/          │     │ tests/          │     │ Live API        │
   │   mocked_data/  │────▶│   fixture_cache/│────▶│ Calls           │
   │                 │     │                 │     │                 │
   │ ✅ Always       │     │ ⚠️  Local only  │     │ ⚠️  Network +   │
   │    Available    │     │                 │     │    Credentials  │
   │ ✅ CI Safe      │     │ 🚀 Fast + Real  │     │ 🔄 Cache Refresh │
   │ ✅ Anonymized   │     │ 📵 Offline OK   │     │ 🎯 Validation   │
   └─────────────────┘     └─────────────────┘     └─────────────────┘
            │                        │                        │
            └────────────────────────┼────────────────────────┘
                                     │
                         AUTOMATIC FALLBACK LOGIC
                                     ▼

┌─────────────────────────────────────────────────────────────────────────────┐
│                              TEST CLASSIFICATION                           │
└─────────────────────────────────────────────────────────────────────────────┘

   🧪 UNIT TESTS           🔧 INTEGRATION          ⚡ PERFORMANCE
   ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
   │ Schema          │     │ End-to-End      │     │ Latency &       │
   │ Validation      │     │ Workflows       │     │ Regression      │
   │                 │     │                 │     │ Testing         │
   │ Data: Mocked    │     │ Data: Any       │     │ Data: Real      │
   │ Speed: Fast     │     │ Speed: Medium   │     │ Speed: Variable │
   │ CI: Always      │     │ CI: w/ Mocked   │     │ CI: Optional    │
   └─────────────────┘     └─────────────────┘     └─────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLI INTERFACE                                 │
└─────────────────────────────────────────────────────────────────────────────┘

pytest --data-source=auto      # Cached → Mocked fallback
pytest --data-source=mocked    # Force mocked (CI safe)
pytest --data-source=cached    # Prefer cached (fast dev)
pytest --data-source=remote    # Force remote (requires creds)

pytest -m unit                 # Unit tests only
pytest -m integration          # Integration tests
pytest -m performance          # Performance tests
pytest -m "not remote"         # Skip remote-dependent

pytest --update                # Refresh cached fixtures
pytest --skip-missing-data     # Skip when data unavailable

┌─────────────────────────────────────────────────────────────────────────────┐
│                             WORKFLOW MATRIX                                │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────────────┐
│   CONTEXT   │   MOCKED    │   CACHED    │   REMOTE    │      USE CASE       │
├─────────────┼─────────────┼─────────────┼─────────────┼─────────────────────┤
│ CI/CD       │ ✅ Primary  │ ❌ N/A      │ ❌ Never    │ Automated testing   │
│ Onboarding  │ ✅ Start    │ ⚠️ Generate │ ❌ Advanced │ New dev setup       │
│ Development │ ✅ Fallback │ ✅ Primary  │ ⚠️ Refresh  │ Daily iteration     │
│ Validation  │ ⚠️ Limited  │ ✅ Good     │ ✅ Best     │ Schema changes      │
│ Performance │ ⚠️ Baseline │ ✅ Good     │ ✅ Real     │ Latency analysis    │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                            SECURITY MODEL                                  │
└─────────────────────────────────────────────────────────────────────────────┘

🔒 SECURITY LEVELS:
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ PUBLIC          │  │ LOCAL ONLY      │  │ CONFIDENTIAL    │
│                 │  │                 │  │                 │
│ • Mocked Data   │  │ • Cached Data   │  │ • Remote Access │
│ • In Repository │  │ • .gitignore    │  │ • Credentials   │
│ • CI Safe       │  │ • Dev Machine   │  │ • Live Servers  │
│ • Anonymized    │  │ • Not Shared    │  │ • Audit Trail   │
└─────────────────┘  └─────────────────┘  └─────────────────┘

📋 COMPLIANCE:
• No sensitive data in repository
• Cached data excluded from version control
• Remote access requires explicit credentials
• Audit trail for production data access

┌─────────────────────────────────────────────────────────────────────────────┐
│                           DEVELOPER JOURNEY                                │
└─────────────────────────────────────────────────────────────────────────────┘

Day 1: 🚀 ONBOARDING
├── git clone repo
├── pip install -e .
├── pytest -m unit                    # ✅ Works immediately
└── pytest -m integration --data-source=mocked

Week 1: 🔄 DEVELOPMENT
├── Set environment variables
├── pytest --update -m remote         # Generate cached data
├── pytest --data-source=cached       # Fast offline development
└── Regular pytest runs               # Auto fallback

Month 1: 🎯 ADVANCED
├── pytest -m performance             # Performance testing
├── Custom fixture creation
├── Remote validation workflows
└── Contributing test improvements

┌─────────────────────────────────────────────────────────────────────────────┐
│                             ERROR HANDLING                                 │
└─────────────────────────────────────────────────────────────────────────────┘

❌ No Data Available
   └── pytest --data-source=mocked  # Use available mocked data
   └── pytest --update -m remote    # Generate cached data

❌ Environment Variables Missing
   └── export HILLTOP_BASE_URL=...
   └── export HILLTOP_HTS_ENDPOINT=...

❌ Network/Credential Issues
   └── pytest -m "not remote"       # Skip remote tests
   └── pytest --data-source=cached  # Use offline data

❌ Schema Changes
   └── Update mocked fixtures
   └── pytest --update              # Refresh cached data
   └── Validate with real data

Legend: ✅ Recommended  ⚠️ Conditional  ❌ Not Available  🔄 Dynamic
```
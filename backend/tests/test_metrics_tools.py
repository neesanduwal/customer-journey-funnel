import unittest

from backend.agent.analytics_agent import analytics_agent
from backend.tools.snapshot_tool import get_snapshot
from backend.tools.running_total_tool import get_running_total
from backend.tools.wow_tool import get_wow
from backend.tools.yoy_tool import get_yoy


class MetricsToolTraceabilityTests(unittest.TestCase):
    def test_traceability_included_in_metric_responses(self):
        snapshot = get_snapshot("local.gold.gold_running_total")
        self.assertIsNotNone(snapshot["snapshot_id"])
        self.assertIsNotNone(snapshot["committed_at"])

        response = get_running_total("2024-01-15")
        self.assertIn("Snapshot ID", response)
        self.assertIn("As-of Date", response)

        response = get_wow("2024-01-15")
        self.assertIn("Snapshot ID", response)
        self.assertIn("As-of Date", response)

        response = get_yoy("2024-01-15")
        self.assertIn("Snapshot ID", response)
        self.assertIn("As-of Date", response)

    def test_weekly_lead_funnel_yoy_question_is_routed_correctly(self):
        response = analytics_agent("How does this week's lead funnel compare to the same week last year?")
        self.assertIn("YoY", response)
        self.assertIn("Date Range", response)
        self.assertIn("Snapshot ID", response)


if __name__ == "__main__":
    unittest.main()

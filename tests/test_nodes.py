import unittest
from nodes.state import DebateState
from nodes.rounds_node import rounds_node
from nodes.memory_node import memory_node
from config import MAX_ROUNDS

class TestDebateNodes(unittest.TestCase):
    def test_rounds_node_increment(self):
        state = {"current_round": 1, "current_agent": "Scientist"}
        new_state = rounds_node(state)
        self.assertEqual(new_state["current_round"], 2)
        self.assertEqual(new_state["current_agent"], "Philosopher")

    def test_rounds_node_max(self):
        # Even if round is 8, it increments to 9, which triggers Judge in the graph condition
        state = {"current_round": 8, "current_agent": "Philosopher"}
        new_state = rounds_node(state)
        self.assertEqual(new_state["current_round"], 9)
        self.assertEqual(new_state["current_agent"], "Scientist") # Loops back but graph will divert

    def test_memory_node(self):
        state = {"messages": [{"round": 1, "agent": "Scientist", "content": "test"}]}
        new_state = memory_node(state)
        self.assertEqual(new_state["messages"], state["messages"])

if __name__ == "__main__":
    unittest.main()

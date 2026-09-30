from collections import deque


class Action:
    def __init__(
        self,
        name,
        positive_preconditions=None,
        negative_preconditions=None,
        positive_effects=None,
        negative_effects=None
    ):
        self.name = name
        self.positive_preconditions = set(
            positive_preconditions or []
        )
        self.negative_preconditions = set(
            negative_preconditions or []
        )
        self.positive_effects = set(
            positive_effects or []
        )
        self.negative_effects = set(
            negative_effects or []
        )


def is_applicable(state, action):
    """
    Check whether all action preconditions are satisfied.
    """

    positive_ok = action.positive_preconditions.issubset(state)

    negative_ok = action.negative_preconditions.isdisjoint(state)

    return positive_ok and negative_ok


def apply_action(state, action):
    """
    Apply an action to a state.

    Negative effects are removed.
    Positive effects are added.
    """

    new_state = set(state)

    new_state.difference_update(action.negative_effects)

    new_state.update(action.positive_effects)

    return new_state


def goal_reached(state, goal):
    """
    Check whether all goal propositions are present.
    """

    return goal.issubset(state)


def breadth_first_search(initial_state, goal, actions):
    """
    Use BFS to search for a sequence of actions that reaches the goal.
    """

    initial_state = frozenset(initial_state)

    queue = deque()

    queue.append(
        (
            initial_state,
            [],
            [initial_state]
        )
    )

    visited = set()

    while queue:

        state, plan, state_history = queue.popleft()

        if goal_reached(state, goal):
            return plan, state_history

        if state in visited:
            continue

        visited.add(state)

        for action in actions:

            if is_applicable(state, action):

                new_state = apply_action(
                    set(state),
                    action
                )

                new_state = frozenset(new_state)

                if new_state not in visited:

                    new_plan = plan + [action.name]

                    new_history = (
                        state_history + [new_state]
                    )

                    queue.append(
                        (
                            new_state,
                            new_plan,
                            new_history
                        )
                    )

    return None, None


def print_plan(plan, state_history):

    if plan is None:
        print("No plan found")
        return

    print("Plan found:")
    print()

    for number, action in enumerate(plan, start=1):
        print(f"{number}. {action}")

    print()
    print("States:")

    for number, state in enumerate(state_history):

        print(f"S{number}:")

        for fact in sorted(state):
            print(f"    {fact}")

        print()


def create_warehouse_actions():

    actions = [

        Action(
            name="Move(A,B)",
            positive_preconditions={
                "At(Robot,A)"
            },
            positive_effects={
                "At(Robot,B)"
            },
            negative_effects={
                "At(Robot,A)"
            }
        ),

        Action(
            name="Move(B,A)",
            positive_preconditions={
                "At(Robot,B)"
            },
            positive_effects={
                "At(Robot,A)"
            },
            negative_effects={
                "At(Robot,B)"
            }
        ),

        Action(
            name="Move(B,C)",
            positive_preconditions={
                "At(Robot,B)"
            },
            positive_effects={
                "At(Robot,C)"
            },
            negative_effects={
                "At(Robot,B)"
            }
        ),

        Action(
            name="Move(C,B)",
            positive_preconditions={
                "At(Robot,C)"
            },
            positive_effects={
                "At(Robot,B)"
            },
            negative_effects={
                "At(Robot,C)"
            }
        ),

        Action(
            name="PickUp(Package,A)",
            positive_preconditions={
                "At(Robot,A)",
                "At(Package,A)"
            },
            positive_effects={
                "Holding(Package)"
            },
            negative_effects={
                "At(Package,A)"
            }
        ),

        Action(
            name="PickUp(Package,B)",
            positive_preconditions={
                "At(Robot,B)",
                "At(Package,B)"
            },
            positive_effects={
                "Holding(Package)"
            },
            negative_effects={
                "At(Package,B)"
            }
        ),

        Action(
            name="PickUp(Package,C)",
            positive_preconditions={
                "At(Robot,C)",
                "At(Package,C)"
            },
            positive_effects={
                "Holding(Package)"
            },
            negative_effects={
                "At(Package,C)"
            }
        ),

        Action(
            name="Drop(Package,A)",
            positive_preconditions={
                "At(Robot,A)",
                "Holding(Package)"
            },
            positive_effects={
                "At(Package,A)"
            },
            negative_effects={
                "Holding(Package)"
            }
        ),

        Action(
            name="Drop(Package,B)",
            positive_preconditions={
                "At(Robot,B)",
                "Holding(Package)"
            },
            positive_effects={
                "At(Package,B)"
            },
            negative_effects={
                "Holding(Package)"
            }
        ),

        Action(
            name="Drop(Package,C)",
            positive_preconditions={
                "At(Robot,C)",
                "Holding(Package)"
            },
            positive_effects={
                "At(Package,C)"
            },
            negative_effects={
                "Holding(Package)"
            }
        )
    ]

    return actions


def run_test(test_name, initial_state, goal, actions):

    print("=" * 60)
    print(test_name)
    print("=" * 60)

    plan, state_history = breadth_first_search(
        initial_state,
        goal,
        actions
    )

    print_plan(plan, state_history)

    print()


if __name__ == "__main__":

    initial_state = {
        "At(Robot,A)",
        "At(Package,A)"
    }

    goal = {
        "At(Package,C)"
    }


    # ==========================================
    # TEST A: Solvable Problem
    # ==========================================

    actions = create_warehouse_actions()

    run_test(
        "TEST A: Solvable Problem",
        initial_state,
        goal,
        actions
    )


    # ==========================================
    # TEST B: Impossible Problem
    # ==========================================

    actions_without_pickup = [
        action
        for action in actions
        if not action.name.startswith("PickUp")
    ]

    run_test(
        "TEST B: Impossible Problem",
        initial_state,
        goal,
        actions_without_pickup
    )


    # ==========================================
    # TEST C: Irrelevant Action
    # ==========================================

    irrelevant_action = Action(
        name="Move(A,B)",
        positive_preconditions={
            "At(Robot,A)"
        },
        positive_effects={
            "At(Robot,B)"
        },
        negative_effects={
            "At(Robot,A)"
        }
    )

    run_test(
        "TEST C: Irrelevant Action",
        initial_state,
        goal,
        [irrelevant_action]
    )
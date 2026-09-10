"""Shared persuasion boundaries used by Vitia assessments and supporting audits."""

DOMAINS = (
    "superbia", "avaritia", "luxuria", "invidia", "gula", "ira", "acedia",
)

BLOCKING_FLAGS = {
    "children_targeting", "acute_vulnerability", "fabricated_claims",
    "deceptive_scarcity", "hidden_default", "discriminatory_targeting",
    "addiction_exploitation", "incitement", "nonconsensual_surveillance",
    "price_obfuscation", "inaccessible_cancellation",
    "paid_random_rewards_children", "loss_chasing_design",
    "unbounded_spend_exploitation", "artificial_friction_for_payment",
}

# Existing supporting audits retain their own heuristic penalties. The Vitia
# 2.0 value/performance profile reports these risks without changing either axis.
RISK_PENALTIES = {
    "unverified_scarcity": ({"avaritia"}, 0.40),
    "status_shaming": ({"superbia", "invidia"}, 0.40),
    "sexual_exploitation": ({"luxuria"}, 0.50),
    "compulsive_loop": ({"luxuria", "gula"}, 0.50),
    "anger_escalation": ({"ira"}, 0.50),
    "coercive_default": ({"acedia"}, 0.50),
    "privacy_intrusion": (set(DOMAINS), 0.30),
}

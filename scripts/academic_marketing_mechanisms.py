#!/usr/bin/env python3
"""Catalog additional academic mechanisms for marketing artifact audits.

These specifications cache routing signals and test guardrails, not effect sizes.
They are kept separate from the audit engine so evidence-driven additions remain
reviewable as data rather than becoming hidden scoring logic.
"""

from __future__ import annotations

from typing import Any


ACADEMIC_MODULES: dict[str, dict[str, Any]] = {
    "regulatory_fit": {
        "domains": ["superbia", "avaritia", "acedia"],
        "opportunity": {
            "goal_orientation_salient": 0.25,
            "promotion_or_prevention_frame_available": 0.20,
            "means_frame_mismatch": 0.20,
            "goal_pursuit_message": 0.20,
            "audience_goal_context_known": 0.15,
        },
        "readiness": {
            "orientation_inferred_from_context": 0.15,
            "matched_and_mismatched_variants": 0.20,
            "claim_strength_held_constant": 0.15,
            "felt_rightness_not_truth_guardrail": 0.15,
            "behavioral_measure_available": 0.20,
            "subgroup_heterogeneity_plan": 0.15,
        },
        "hypothesis": (
            "Matching a contextually salient promotion or prevention goal with "
            "compatible eager or vigilant means may change engagement and value."
        ),
        "test": (
            "Cross goal framing with matched and mismatched means while holding "
            "claims constant; measure qualified action, comprehension, and trust."
        ),
        "caution": (
            "Regulatory fit can make a message feel right without making it true. "
            "Infer orientation from the decision context, not a personality label."
        ),
    },
    "construal_alignment": {
        "domains": ["luxuria", "avaritia", "acedia"],
        "opportunity": {
            "psychological_distance_relevant": 0.25,
            "near_or_far_horizon": 0.20,
            "feasibility_desirability_tradeoff": 0.20,
            "abstract_concrete_mismatch": 0.20,
            "action_stage_known": 0.15,
        },
        "readiness": {
            "distance_context_documented": 0.20,
            "matched_message_pair": 0.20,
            "facts_identical_across_levels": 0.15,
            "comprehension_measure": 0.15,
            "action_quality_measure": 0.15,
            "overgeneralization_guardrail": 0.15,
        },
        "hypothesis": (
            "Aligning abstract purpose with distant evaluation and concrete "
            "feasibility with near action may improve evaluation or execution."
        ),
        "test": (
            "Cross abstract versus concrete framing with near versus distant "
            "decision context while preserving facts; measure comprehension and "
            "qualified action."
        ),
        "caution": (
            "Psychological distance is multidimensional and effects are contextual. "
            "Do not replace material details with abstraction at any distance."
        ),
    },
    "self_determination": {
        "domains": ["superbia", "gula", "acedia"],
        "opportunity": {
            "sustained_engagement_goal": 0.20,
            "autonomy_relevance": 0.20,
            "competence_relevance": 0.20,
            "relatedness_relevance": 0.15,
            "controlling_language_present": 0.15,
            "internalization_required": 0.10,
        },
        "readiness": {
            "meaningful_choice_available": 0.15,
            "rationale_disclosed": 0.15,
            "competence_feedback_truthful": 0.20,
            "relatedness_nonpressuring": 0.15,
            "opt_out_easy": 0.15,
            "wellbeing_or_quality_measure": 0.10,
            "no_dependency_design": 0.10,
        },
        "hypothesis": (
            "Supporting meaningful choice, truthful competence feedback, and "
            "nonpressuring connection may improve autonomous engagement."
        ),
        "test": (
            "Compare an autonomy-supportive treatment with the current treatment; "
            "measure sustained qualified use, perceived pressure, and easy exit."
        ),
        "caution": (
            "Basic psychological needs are not engagement hacks. Superficial choice, "
            "dependency, and belonging pressure can undermine autonomy."
        ),
    },
    "goal_gradient": {
        "domains": ["gula", "acedia", "avaritia"],
        "opportunity": {
            "multi_step_goal": 0.20,
            "progress_observable": 0.20,
            "distance_to_goal_variable": 0.20,
            "completion_dropoff_observed": 0.20,
            "existing_progress_can_be_credited": 0.20,
        },
        "readiness": {
            "progress_is_real": 0.20,
            "goal_and_reward_disclosed": 0.15,
            "reset_expiry_disclosed": 0.15,
            "incremental_value_preserved": 0.15,
            "overuse_guardrail": 0.15,
            "abandonment_or_regret_measure": 0.10,
            "no_sunk_cost_pressure": 0.10,
        },
        "hypothesis": (
            "Visible, truthful progress toward a valued goal may increase effort as "
            "the remaining distance becomes smaller."
        ),
        "test": (
            "Randomize a truthful progress representation or credit for completed "
            "work; measure completion, pace, overuse, abandonment, and regret."
        ),
        "caution": (
            "Do not fabricate head starts, conceal resets, or turn accumulated "
            "progress into sunk-cost pressure or compulsive use."
        ),
    },
    "information_scent": {
        "domains": ["acedia", "avaritia"],
        "opportunity": {
            "search_or_navigation_task": 0.25,
            "information_need_known": 0.15,
            "path_uncertainty": 0.20,
            "competing_routes": 0.15,
            "label_target_mismatch": 0.15,
            "decision_information_distributed": 0.10,
        },
        "readiness": {
            "target_information_defined": 0.20,
            "cue_target_mapping_verified": 0.20,
            "path_cost_measured": 0.15,
            "representative_tasks": 0.15,
            "findability_measure": 0.15,
            "no_material_information_hiding": 0.15,
        },
        "hypothesis": (
            "Truthful cues that better predict the value and location of target "
            "information may reduce search cost and navigation failure."
        ),
        "test": (
            "Change cue wording or placement while holding the destination constant; "
            "measure findability, path cost, comprehension, and misclicks."
        ),
        "caution": (
            "Information scent depends on the user's goal and vocabulary. Clicks "
            "alone do not show that the destination answered the information need."
        ),
    },
    "elaboration_depth": {
        "domains": ["avaritia", "superbia", "acedia"],
        "opportunity": {
            "consequential_decision": 0.20,
            "involvement_or_relevance_high": 0.20,
            "motivation_to_scrutinize": 0.20,
            "ability_to_scrutinize": 0.20,
            "claim_complexity": 0.20,
        },
        "readiness": {
            "argument_quality_supported": 0.20,
            "material_evidence_accessible": 0.20,
            "peripheral_cues_separable": 0.15,
            "involvement_context_measured": 0.15,
            "delayed_or_resistant_outcome": 0.15,
            "no_distraction_from_terms": 0.15,
        },
        "hypothesis": (
            "When motivation and ability to scrutinize are high, supported argument "
            "quality should matter more than incidental peripheral cues."
        ),
        "test": (
            "Vary argument quality separately from a peripheral cue and measure "
            "immediate and delayed judgment, comprehension, and resistance."
        ),
        "caution": (
            "Elaboration is a situated continuum, not a type of person. Never reduce "
            "ability or hide terms to make peripheral cues more influential."
        ),
    },
    "credible_signaling": {
        "domains": ["superbia", "avaritia"],
        "opportunity": {
            "quality_unobservable_pre_purchase": 0.25,
            "information_asymmetry": 0.20,
            "trust_deficit": 0.15,
            "warranty_or_commitment_available": 0.20,
            "verification_delay": 0.10,
            "seller_bears_failure_cost": 0.10,
        },
        "readiness": {
            "signal_cost_or_bond_real": 0.20,
            "quality_signal_link_explained": 0.15,
            "terms_verifiable": 0.20,
            "remedy_enforceable": 0.20,
            "adverse_selection_considered": 0.10,
            "no_empty_badges": 0.15,
        },
        "hypothesis": (
            "A verifiable commitment that makes failure costly to the seller may "
            "reduce quality uncertainty when it is credible and enforceable."
        ),
        "test": (
            "Vary the verified commitment while holding product claims constant; "
            "measure quality inference, comprehension of terms, trust, and claims."
        ),
        "caution": (
            "Costly does not automatically mean credible. Warranties and badges can "
            "backfire when conditions are obscure or the quality link is weak."
        ),
    },
}

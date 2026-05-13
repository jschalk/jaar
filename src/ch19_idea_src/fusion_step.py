from pandas import DataFrame as pandas_DataFrame, concat as pandas_concat


def fusion_add_ancestor_rope_rows(
    df: pandas_DataFrame, config: dict
) -> pandas_DataFrame:
    KNOT = ";"

    if "plan_rope" not in df.columns:
        return df

    existing_ropes = set(df["plan_rope"].dropna().unique())
    new_rows = []
    for _, row in df.iterrows():
        rope = row["plan_rope"]
        if not isinstance(rope, str):
            continue
        segments = [s for s in rope.split(KNOT) if s]
        for i in range(1, len(segments)):
            ancestor = KNOT + KNOT.join(segments[:i]) + KNOT
            if ancestor not in existing_ropes:
                existing_ropes.add(ancestor)
                new_rows.append(
                    {
                        **row.to_dict(),
                        "plan_rope": ancestor,
                        "pledge": 0,
                    }
                )

    if not new_rows:
        return df

    return pandas_concat([df, pandas_DataFrame(new_rows)], ignore_index=True)


def fusion_set_pledge_to_one(df: pandas_DataFrame, config: dict) -> pandas_DataFrame:
    df = df.copy()
    df["pledge"] = 1
    return df


def fusion_set_plan_rope_from_health_label(
    df: pandas_DataFrame, config: dict
) -> pandas_DataFrame:
    if "moment_rope" not in df.columns:
        raise ValueError(
            "fusion_set_plan_rope_from_health_label requires a 'moment_rope' column but it was not found. "
            f"Columns present: {list(df.columns)}"
        )
    if "health_label" not in df.columns:
        raise ValueError(
            "fusion_set_plan_rope_from_health_label requires a 'health_label' column but it was not found. "
            f"Columns present: {list(df.columns)}"
        )

    null_moment = df["moment_rope"].isnull()
    if null_moment.any():
        bad_indices = df.index[null_moment].tolist()
        raise ValueError(
            f"fusion_set_plan_rope_from_health_label found null values in 'moment_rope' at row indices: {bad_indices}. "
            "Every row must have a valid moment_rope value to construct plan_rope."
        )

    null_health = df["health_label"].isnull()
    if null_health.any():
        bad_indices = df.index[null_health].tolist()
        raise ValueError(
            f"fusion_set_plan_rope_from_health_label found null values in 'health_label' at row indices: {bad_indices}. "
            "Every row must have a valid health_label value to construct plan_rope."
        )

    df = df.copy()
    df["plan_rope"] = df["moment_rope"] + "health;" + df["health_label"] + ";"
    return df


def fusion_set_moment_rope_from_moment_label(
    df: pandas_DataFrame, config: dict
) -> pandas_DataFrame:
    if "moment_label" not in df.columns:
        raise ValueError(
            "fusion_set_moment_rope_from_moment_label requires a 'moment_label' column but it was not found. "
            f"Columns present: {list(df.columns)}"
        )

    null_moment_label = df["moment_label"].isnull()
    if null_moment_label.any():
        bad_indices = df.index[null_moment_label].tolist()
        raise ValueError(
            f"fusion_set_moment_rope_from_moment_label found null values in 'moment_label' at row indices: {bad_indices}. "
            "Every row must have a valid moment_label value to construct moment_rope."
        )

    df = df.copy()
    df["moment_rope"] = ";" + df["moment_label"] + ";"
    return df


def fusion_add_knot_from_rope(df: pandas_DataFrame, config: dict) -> pandas_DataFrame:
    if "knot" in df.columns:
        return df

    knot = None

    for col in ["moment_rope", "plan_rope"]:
        if col in df.columns:
            first_valid = None if df[col].dropna().empty else df[col].dropna().iloc[0]
            if first_valid is not None and len(first_valid) > 0:
                knot = first_valid[0]
                break

    if knot is None:
        knot = ";"

    df = df.copy()
    df["knot"] = knot
    return df

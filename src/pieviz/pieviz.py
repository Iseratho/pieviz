import re

import numpy as np
from typing import Dict, Union

import pandas as pd
import plotly.graph_objects as go
import plotly.io


DEFAULT_FIG_WIDTH = 1184
DEFAULT_FIG_HEIGHT = 784
DEFAULT_DPI = 96


def bake_all_pies_from_csv(csv_file: str, prefix: str = "") -> None:
    df = pd.read_csv(csv_file, index_col=0)

    for index, row in df.iterrows():
        title = f"{prefix}{index}"
        data = row.to_dict()
        print(title, data)
        fig = bake_pie(data)
        store_pie(fig, f"{prefix}{index}.png", format="png")


def bake_and_store_pie(
    data_dict: Dict[str, Union[int, float]],
    output_file: str,
    font_size: int = 42,
) -> None:
    fig = bake_pie(data_dict, font_size=font_size)
    store_pie(fig, output_file)


def store_pie(fig: go.Figure, output_file: str, format: str | None = None) -> None:
    """
    Save Plotly figure as file.

    Args:
        fig (plotly.graph_objects.Figure): The Plotly figure to save
        output_file (str): Output file path
        format (str): Output format ('html', 'png', 'svg', 'pdf', etc.)
    """
    if format == "html" or format is None and output_file.lower().endswith(".html"):
        fig.write_html(output_file)
    else:
        width = (
            int(fig.layout.width) if fig.layout.width is not None else DEFAULT_FIG_WIDTH
        )
        height = (
            int(fig.layout.height)
            if fig.layout.height is not None
            else DEFAULT_FIG_HEIGHT
        )
        try:
            fig.write_image(
                output_file,
                format=format,
                width=width,
                height=height,
            )
        except RuntimeError:
            # install chrome and try again
            plotly.io.get_chrome()
            fig.write_image(
                output_file,
                format=format,
                width=width,
                height=height,
            )
    print(f"Chart saved as {output_file}")


def _create_pie_slices_mesh(
    start_angle: float,
    end_angle: float,
    angle_step_size: float = np.pi / 20,
    radius: float = 1.0,
    height: float = 0.1,
) -> tuple[np.ndarray, np.ndarray]:
    # create 3D wedge slice using mesh geometry
    theta = np.linspace(
        start_angle,
        end_angle,
        int((end_angle - start_angle) / angle_step_size) + 1,
        endpoint=True,
    )
    points = []
    triangles = []

    def add_point(x, y, z):
        point_index = len(points)
        points.append((x, y, z))
        return point_index

    def add_points(points_array):
        indices = []
        for x, y, z in points_array:
            indices.append(add_point(x, y, z))
        return indices

    def add_triangle(i, j, k):
        triangles.append((i, j, k))

    def add_quad(left_bot_i, right_bot_i, right_top_i, left_top_i):
        add_triangle(left_bot_i, right_bot_i, right_top_i)
        add_triangle(left_bot_i, right_top_i, left_top_i)

    # height scaling
    inner_bottom_point_idx = add_point(0, 0, 0)
    inner_top_point_idx = add_point(0, 0, height)

    # start plane
    start_outer_bottom_point_idx = add_point(
        radius * np.cos(start_angle), radius * np.sin(start_angle), 0
    )
    start_outer_top_point_idx = add_point(
        radius * np.cos(start_angle), radius * np.sin(start_angle), height
    )
    add_quad(
        inner_bottom_point_idx,
        start_outer_bottom_point_idx,
        start_outer_top_point_idx,
        inner_top_point_idx,
    )

    # end plane
    end_outer_bottom_point_idx = add_point(
        radius * np.cos(end_angle), radius * np.sin(end_angle), 0
    )
    end_outer_top_point_idx = add_point(
        radius * np.cos(end_angle), radius * np.sin(end_angle), height
    )
    add_quad(
        inner_bottom_point_idx,
        end_outer_bottom_point_idx,
        end_outer_top_point_idx,
        inner_top_point_idx,
    )

    # curved surface
    theta_without_start_end = theta[
        1:-1
    ]  # remove start and end angles since they are covered by the planes
    outer_bottom_curved_points = np.stack(
        (
            radius * np.cos(theta_without_start_end),
            radius * np.sin(theta_without_start_end),
            np.zeros_like(theta_without_start_end),
        ),
        axis=-1,
    )
    outer_bottom_curved_idx = add_points(outer_bottom_curved_points)
    outer_top_curved_points = np.stack(
        (
            radius * np.cos(theta_without_start_end),
            radius * np.sin(theta_without_start_end),
            np.full_like(theta_without_start_end, height),
        ),
        axis=-1,
    )
    outer_top_curved_idx = add_points(outer_top_curved_points)

    outer_point_idxs = (
        [(start_outer_bottom_point_idx, start_outer_top_point_idx)]
        + list(zip(outer_bottom_curved_idx, outer_top_curved_idx))
        + [(end_outer_bottom_point_idx, end_outer_top_point_idx)]
    )
    for (prev_outer_bottom_point_idx, prev_outer_top_point_idx), (
        bottom_point_idx,
        top_point_idx,
    ) in zip(outer_point_idxs[:-1], outer_point_idxs[1:]):
        # add outside quad
        add_quad(
            prev_outer_bottom_point_idx,
            bottom_point_idx,
            top_point_idx,
            prev_outer_top_point_idx,
        )

        # add top triangle
        add_triangle(prev_outer_top_point_idx, top_point_idx, inner_top_point_idx)
        # add bottom triangle
        add_triangle(
            prev_outer_bottom_point_idx, inner_bottom_point_idx, bottom_point_idx
        )

    points, triangles = np.array(points), np.array(triangles)
    return points, triangles


def bake_pie(
    data_dict: Dict[str, Union[int, float]],
    radius: float = 1.0,
    height: float = 0.3,
    font_size: int = 42,
    label_with_percent: bool = False,
    small_slice_labels_outside: bool = False,
    projection_type: str = "orthographic",
    colors: list[str] = ['#3366cc', '#dc3912', '#ff9900', '#109618']
) -> go.Figure:
    """
    Create a true 3D pie chart using Mesh3d triangulation.
    Each slice is rendered as a 3D wedge using mesh geometry.

    Args:
        data_dict (dict): Dictionary with labels as keys and values as numeric values
        title (str): Title for the pie chart

    Returns:
        plotly.graph_objects.Figure: The 3D mesh pie chart figure
    """
    labels = list(data_dict.keys())
    values = np.array(list(data_dict.values()), dtype=float)

    # exclude empty slices (0 or negative values)
    valid_indices = values > 0
    labels = [label for label, valid in zip(labels, valid_indices) if valid]
    values = values[valid_indices]

    # Normalize values to angles
    total = values.sum()
    angles = 2 * np.pi * values / total
    angles = [0] + list(angles)  # add starting angle for cumulative sum
    angles = np.cumsum(angles)  # cumulative sum to get start/end angles for each slice

    fig = go.Figure()

    annotations = []
    is_single_slice = len(labels) == 1
    for i, (label, (start_angle, end_angle)) in enumerate(
        zip(labels, zip(angles[:-1], angles[1:]))
    ):
        points, triangles = _create_pie_slices_mesh(
            start_angle, end_angle, radius=radius, height=height
        )
        fig.add_trace(
            go.Mesh3d(
                x=points[:, 0],
                y=points[:, 1],
                z=points[:, 2],
                i=triangles[:, 0],
                j=triangles[:, 1],
                k=triangles[:, 2],
                name=label,
                text=label,
                showlegend=False,
                showscale=False,
                color=colors[i % len(colors)],
                hovertext=f"{label} ({values[i] / total * 100:.1f}%)"
                if label_with_percent
                else label,
                hoverinfo="text",
                flatshading=True,
            )
        )

        annotation_x = 0.0
        annotation_y = 0.0
        showarrow = False
        ax = 0
        ay = 0
        if is_single_slice:
            annotation_x = 0.0
            annotation_y = 0.0
            showarrow = False
            ax = 0
            ay = 0
        elif (
            end_angle - start_angle < np.pi / 50
        ) and small_slice_labels_outside:  # if slice is too small, put annotation outside
            showarrow = True
            annotation_x = radius * 1.0 * np.cos((start_angle + end_angle) / 2)
            annotation_y = radius * 1.0 * np.sin((start_angle + end_angle) / 2)
            ax = -150 * np.cos((start_angle + end_angle + np.pi / 2) / 2)
            ay = 50 * np.sin((start_angle + end_angle + np.pi / 2) / 2)
            font = dict(size=font_size, color="black")
        else:
            showarrow = False
            if i % 2 == 0:
                annotation_x = radius * 0.7 * np.cos((start_angle + end_angle) / 2)
                annotation_y = radius * 0.7 * np.sin((start_angle + end_angle) / 2)
            else:
                annotation_x = radius * 0.4 * np.cos((start_angle + end_angle) / 2)
                annotation_y = radius * 0.4 * np.sin((start_angle + end_angle) / 2)
        font = dict(size=font_size, color="white")
        if end_angle - start_angle < np.pi / 10:
            angle_size = (end_angle - start_angle)
            font = dict(size=max(font_size * angle_size / (np.pi / 10), 10), color="white")

        if "pie" in label.lower():
            # lower or upper case
            label = re.sub(r"(?i)pie", "🥧", label).strip()

        annotations.append(
            dict(
                x=annotation_x,
                y=annotation_y,
                z=height,
                text=label
                if not label_with_percent
                else f"{label} ({values[i] / total * 100:.1f}%)",
                arrowsize=1,
                arrowwidth=4,
                showarrow=showarrow,
                ax=ax,
                ay=ay,
                font=font,
            )
        )

    range_val = radius * 1.5
    zoom = 3.0
    fig.update_layout(
        # title=dict(text=title, x=0.5, xanchor="center"),
        scene=dict(
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                visible=False,
                range=[-range_val, range_val],
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                visible=False,
                range=[-range_val, range_val],
            ),
            zaxis=dict(
                showgrid=False,
                zeroline=False,
                visible=False,
                range=[-range_val, range_val],
            ),
            annotations=annotations,
            # reposition camera
            camera=dict(
                eye=dict(x=radius, y=radius, z=1.8 * radius),
                projection=dict(type=projection_type),
            ),
            aspectratio=dict(x=zoom, y=zoom, z=zoom),
        ),
        title_font=dict(size=font_size + 4, color="black"),
        font=dict(size=font_size, color="black"),
        showlegend=False,
        margin=dict(l=0, r=0, b=0, t=50),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig

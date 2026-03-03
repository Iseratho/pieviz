import os
import tempfile
import unittest
from unittest import mock

import numpy as np
import plotly.graph_objects as go

import pieviz
from pieviz.pieviz import (
    DEFAULT_FIG_HEIGHT,
    DEFAULT_FIG_WIDTH,
    _create_pie_slices_mesh,
)


class TestPie(unittest.TestCase):
    def setUp(self):
        self.test_data = {"A": 30, "B": 50, "C": 20}

    def test_bake_pie_returns_mesh3d_traces(self):
        fig = pieviz.bake_pie(self.test_data)

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == len(self.test_data)
        assert all(isinstance(trace, go.Mesh3d) for trace in fig.data)
        assert fig.layout.showlegend is False
        assert fig.layout.scene.camera.projection.type == "orthographic"

    def test_bake_pie_single_slice_annotation_is_centered(self):
        fig = pieviz.bake_pie({"Single": 100})

        assert len(fig.layout.scene.annotations) == 1
        annotation = fig.layout.scene.annotations[0]
        assert annotation.x == 0.0
        assert annotation.y == 0.0
        assert annotation.showarrow is False

    def test_bake_pie_percent_labels_and_projection(self):
        fig = pieviz.bake_pie(
            {"X": 1, "Y": 1},
            label_with_percent=True,
            projection_type="perspective",
            colors=["#123456", "#abcdef"],
        )

        assert "(" in fig.data[0].hovertext
        assert "%" in fig.data[0].hovertext
        assert "(" in fig.layout.scene.annotations[0].text
        assert fig.data[0].color == "#123456"
        assert fig.layout.scene.camera.projection.type == "perspective"

    def test_store_pie_writes_html_when_extension_matches(self):
        fig = pieviz.bake_pie(self.test_data)
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, "mesh.html")
            pieviz.store_pie(fig, output_file)

            assert os.path.exists(output_file)
            assert os.path.getsize(output_file) > 0
            with open(output_file, "r", encoding="utf-8") as file:
                content = file.read().lower()
            assert "plotly" in content

    def test_store_pie_uses_default_dimensions_for_image(self):
        fig = pieviz.bake_pie(self.test_data)
        with mock.patch.object(fig, "write_image") as write_image:
            pieviz.store_pie(fig, "out.png", format="png")

        write_image.assert_called_once_with(
            "out.png",
            format="png",
            width=DEFAULT_FIG_WIDTH,
            height=DEFAULT_FIG_HEIGHT,
        )

    def test_store_pie_fallback_installs_chrome_then_retries(self):
        fig = pieviz.bake_pie(self.test_data)
        with (
            mock.patch.object(
                fig,
                "write_image",
                side_effect=[RuntimeError("missing chrome"), None],
            ) as write_image,
            mock.patch("pieviz.pieviz.plotly.io.get_chrome") as get_chrome,
        ):
            pieviz.store_pie(fig, "out.png", format="png")

        assert write_image.call_count == 2
        get_chrome.assert_called_once()

    def test_bake_and_store_pie_calls_bake_then_store(self):
        fake_fig = object()
        with (
            mock.patch("pieviz.pieviz.bake_pie", return_value=fake_fig) as bake,
            mock.patch("pieviz.pieviz.store_pie") as store,
        ):
            pieviz.bake_and_store_pie({"A": 1}, "output.html", font_size=22)

        bake.assert_called_once_with({"A": 1}, font_size=22)
        store.assert_called_once_with(fake_fig, "output.html")

    def test_bake_all_pies_from_csv_calls_bake_and_store_for_each_row(self):
        csv_content = "label,a,b\nrow1,1,2\nrow2,3,4\n"
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "input.csv")
            with open(csv_path, "w", encoding="utf-8") as file:
                file.write(csv_content)

            with (
                mock.patch("pieviz.pieviz.bake_pie", return_value="fig") as bake,
                mock.patch("pieviz.pieviz.store_pie") as store,
            ):
                pieviz.bake_all_pies_from_csv(csv_path, prefix="PRE-")

        assert bake.call_count == 2
        bake.assert_any_call({"a": 1, "b": 2})
        bake.assert_any_call({"a": 3, "b": 4})
        store.assert_any_call("fig", "pie/pie_row1.png", format="png")
        store.assert_any_call("fig", "pie/pie_row2.png", format="png")

    def test_create_pie_slices_mesh_outputs_valid_shapes(self):
        points, triangles = _create_pie_slices_mesh(0.0, np.pi / 2)

        assert isinstance(points, np.ndarray)
        assert isinstance(triangles, np.ndarray)
        assert points.ndim == 2 and points.shape[1] == 3
        assert triangles.ndim == 2 and triangles.shape[1] == 3
        assert points.shape[0] > 0
        assert triangles.shape[0] > 0

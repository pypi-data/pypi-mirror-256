import numpy as np
import pytest
from astropy.io import fits
from PIL import ImageDraw

from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.codecs.fits import fits_hdulist_encoder
from dkist_processing_common.models.constants import BudName
from dkist_processing_common.models.fits_access import FitsAccessBase
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks.assemble_movie import AssembleMovie
from dkist_processing_common.tests.conftest import FakeGQLClient


class CompletedAssembleMovie(AssembleMovie):
    def write_overlay(self, draw: ImageDraw, fits_obj: FitsAccessBase):
        self.write_line(draw, f"INSTRUMENT: FOO", 1, column="left", fill="red", font=self.font_18)
        self.write_line(
            draw,
            f"WAVELENGTH: {fits_obj.wavelength}",
            2,
            column="middle",
            fill="blue",
            font=self.font_15,
        )
        self.write_line(
            draw,
            f"OBS TIME: {fits_obj.time_obs}",
            3,
            column="right",
            fill="green",
            font=self.font_18,
        )


# TODO: This fixture should use an L1 only header
# TODO: Figure out how to make this do fuzzy testing on num_dsps_repeats. The issue is that randomization on import borks xdist
@pytest.fixture(
    scope="function", params=[pytest.param(i, id=f"dsps_repeats_{i}") for i in [10, 50]]
)
def assemble_task_with_tagged_movie_frames(
    tmp_path, complete_l1_only_header, recipe_run_id, request
):
    num_dsps_repeats = request.param
    with CompletedAssembleMovie(
        recipe_run_id=recipe_run_id, workflow_name="vbi_make_movie_frames", workflow_version="VX.Y"
    ) as task:
        task.scratch = WorkflowFileSystem(scratch_base_path=tmp_path, recipe_run_id=recipe_run_id)
        task.constants._update(
            {
                BudName.num_dsps_repeats.value: num_dsps_repeats,
                BudName.recipe_run_id.value: recipe_run_id,
            }
        )
        for d in range(num_dsps_repeats):
            data = np.ones((100, 100))
            data[: d * 10, :] = 0.0
            hdl = fits.HDUList(fits.PrimaryHDU(data=data, header=complete_l1_only_header))
            hdl[0].header["DKIST009"] = d + 1
            task.write(
                data=hdl,
                tags=[
                    Tag.movie_frame(),
                    Tag.dsps_repeat(d + 1),
                ],
                encoder=fits_hdulist_encoder,
            )
        yield task
        task._purge()


def test_assemble_movie(assemble_task_with_tagged_movie_frames, mocker):
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    assemble_task_with_tagged_movie_frames()
    movie_file = list(assemble_task_with_tagged_movie_frames.read(tags=[Tag.movie()]))
    assert len(movie_file) == 1
    assert movie_file[0].exists()

    ## Uncomment the following line if you want to actually see the movie
    # os.system(f"cp {movie_file[0]} foo.mp4")

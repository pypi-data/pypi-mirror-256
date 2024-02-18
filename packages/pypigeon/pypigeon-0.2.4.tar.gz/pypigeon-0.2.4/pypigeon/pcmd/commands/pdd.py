from pypigeon import item_io

from .base_commands import BaseCommands


class PddCommands(BaseCommands):
    """Operations on PDDs (data dictionaries)"""

    @BaseCommands._with_arg("collection_id")
    @BaseCommands._with_arg("filename")
    @BaseCommands._with_arg("--item-name")
    @BaseCommands._with_arg("--folder-id", default="ROOT")
    def upload(self) -> None:
        """Upload a PDD from a local file."""

        item_name = self.args.item_name or self.args.filename
        writer = item_io.PigeonItemCreatorText(
            self.args.collection_id,
            "LIVE",
            item_name,
            self.core,
            folder_id=self.args.folder_id,
            type="dictionary",
        )
        with writer as ofp:
            with open(self.args.filename) as ifp:
                ofp.write(ifp.read())

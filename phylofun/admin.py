from django.contrib import admin

from phylofun.models import (
    NetworkModel,
    RearrangementProblemModel,
    RearrangementSolutionModel,
)


@admin.register(NetworkModel)
class NetworkAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "binary",
        "number_of_roots",
        "number_of_leaves",
        "reticulation_number",
    )  # TODO add rearrangement problems


@admin.register(RearrangementProblemModel)
class RearrangementProblemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "network1",
        "network2",
        "move_type",
    )  # TODO add best solution length


@admin.register(RearrangementSolutionModel)
class RearrangementSolutionAdmin(admin.ModelAdmin):
    list_display = ("id", "problem")  # TODO add solution length

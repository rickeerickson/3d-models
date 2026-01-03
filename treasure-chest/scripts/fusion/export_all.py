#Author-
#Description-Export all components to STL

import adsk.core
import adsk.fusion
import os
import traceback

# Configuration
OUTPUT_DIR = "exports/stl"
MESH_REFINEMENT = adsk.fusion.MeshRefinementSettings.MeshRefinementMedium
VERSION = "v01"
MATERIAL = "pla"

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)

        if not design:
            ui.messageBox('No active design found.')
            return

        # Get document directory for export path
        doc = app.activeDocument
        if not doc.isSaved:
            ui.messageBox('Please save the document first.')
            return

        # Get the root component
        root_comp = design.rootComponent

        # Create export manager
        export_mgr = design.exportManager

        # Track exports
        exported = []

        # Export each occurrence (component instance)
        for occ in root_comp.allOccurrences:
            comp = occ.component
            comp_name = comp.name.lower().replace(' ', '-')

            # Skip empty components
            if comp.bRepBodies.count == 0:
                continue

            # Build filename: treasure-chest_{component}_v01_pla.stl
            filename = f"treasure-chest_{comp_name}_{VERSION}_{MATERIAL}.stl"

            # For now, print what would be exported
            # (Full path handling would need document path access)
            exported.append(filename)

        # Also check root component bodies
        for body in root_comp.bRepBodies:
            body_name = body.name.lower().replace(' ', '-')
            filename = f"treasure-chest_{body_name}_{VERSION}_{MATERIAL}.stl"
            exported.append(filename)

        if exported:
            ui.messageBox(f'Would export {len(exported)} files:\n' + '\n'.join(exported))
        else:
            ui.messageBox('No bodies found to export.')

    except:
        if ui:
            ui.messageBox(f'Failed:\n{traceback.format_exc()}')


def stop(context):
    pass

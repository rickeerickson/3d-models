#Author-
#Description-Read and display all user parameters

import adsk.core
import adsk.fusion
import traceback


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)

        if not design:
            ui.messageBox('No active design found.')
            return

        # Get user parameters
        user_params = design.userParameters

        if user_params.count == 0:
            ui.messageBox('No user parameters defined.\n\nAdd parameters via:\nModify > Change Parameters > + (User Parameters)')
            return

        # Build parameter table
        lines = ['User Parameters:', '-' * 40]

        for param in user_params:
            name = param.name
            value = param.value  # Internal units (cm)
            expr = param.expression  # User-entered expression
            unit = param.unit

            # Convert cm to mm for display
            if unit == 'mm':
                display_val = value * 10  # cm to mm
            else:
                display_val = value

            lines.append(f'{name}: {display_val:.2f} {unit} (expr: {expr})')

        ui.messageBox('\n'.join(lines))

    except:
        if ui:
            ui.messageBox(f'Failed:\n{traceback.format_exc()}')


def stop(context):
    pass

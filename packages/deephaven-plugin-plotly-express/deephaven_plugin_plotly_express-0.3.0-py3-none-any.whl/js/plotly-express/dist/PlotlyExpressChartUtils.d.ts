import type { Data, PlotlyDataLayoutConfig } from 'plotly.js';
import type { Widget } from '@deephaven/jsapi-types';
export interface PlotlyChartWidgetData {
    type: string;
    figure: {
        deephaven: {
            mappings: Array<{
                table: number;
                data_columns: Record<string, string[]>;
            }>;
            is_user_set_template: boolean;
            is_user_set_color: boolean;
        };
        plotly: PlotlyDataLayoutConfig;
    };
    revision: number;
    new_references: number[];
    removed_references: number[];
}
export declare function getWidgetData(widgetInfo: Widget): PlotlyChartWidgetData;
export declare function getDataMappings(widgetData: PlotlyChartWidgetData): Map<number, Map<string, string[]>>;
/**
 * Applies the colorway to the data unless the data color is not its default value
 * Data color is not default if the user set the color specifically or the plot type sets it
 *
 * @param colorway The colorway from the web UI
 * @param plotlyColorway The colorway from plotly
 * @param data The data to apply the colorway to. This will be mutated
 */
export declare function applyColorwayToData(colorway: string[], plotlyColorway: string[], data: Data[]): void;
//# sourceMappingURL=PlotlyExpressChartUtils.d.ts.map
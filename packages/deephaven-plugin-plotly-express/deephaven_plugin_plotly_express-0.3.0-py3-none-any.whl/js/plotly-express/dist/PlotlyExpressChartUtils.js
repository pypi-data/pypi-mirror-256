import Log from '@deephaven/log';
const log = Log.module('@deephaven/js-plugin-plotly-express.ChartUtils');
export function getWidgetData(widgetInfo) {
    return JSON.parse(widgetInfo.getDataAsString());
}
export function getDataMappings(widgetData) {
    const data = widgetData.figure;
    // Maps a reference index to a map of column name to an array of the paths where its data should be
    const tableColumnReplacementMap = new Map();
    data.deephaven.mappings.forEach(({ table: tableIndex, data_columns: dataColumns }) => {
        var _a;
        const existingColumnMap = (_a = tableColumnReplacementMap.get(tableIndex)) !== null && _a !== void 0 ? _a : new Map();
        tableColumnReplacementMap.set(tableIndex, existingColumnMap);
        // For each { columnName: [replacePaths] } in the object, add to the tableColumnReplacementMap
        Object.entries(dataColumns).forEach(([columnName, paths]) => {
            const existingPaths = existingColumnMap.get(columnName);
            if (existingPaths !== undefined) {
                existingPaths.push(...paths);
            }
            else {
                existingColumnMap.set(columnName, [...paths]);
            }
        });
    });
    return tableColumnReplacementMap;
}
/**
 * Applies the colorway to the data unless the data color is not its default value
 * Data color is not default if the user set the color specifically or the plot type sets it
 *
 * @param colorway The colorway from the web UI
 * @param plotlyColorway The colorway from plotly
 * @param data The data to apply the colorway to. This will be mutated
 */
export function applyColorwayToData(colorway, plotlyColorway, data) {
    if (colorway.length === 0) {
        return;
    }
    if (plotlyColorway.length > colorway.length) {
        log.warn("Plotly's colorway is longer than the web UI colorway. May result in incorrect colors for some series");
    }
    const colorMap = new Map(plotlyColorway.map((color, i) => {
        var _a;
        return [
            color.toUpperCase(),
            (_a = colorway[i]) !== null && _a !== void 0 ? _a : color,
        ];
    }));
    const plotlyColors = new Set(plotlyColorway.map(color => color.toUpperCase()));
    for (let i = 0; i < data.length; i += 1) {
        const trace = data[i];
        // There are multiple datatypes in plotly and some don't contain marker or marker.color
        if ('marker' in trace &&
            trace.marker != null &&
            'color' in trace.marker &&
            typeof trace.marker.color === 'string') {
            if (plotlyColors.has(trace.marker.color.toUpperCase())) {
                trace.marker.color = colorMap.get(trace.marker.color.toUpperCase());
            }
        }
        if ('line' in trace &&
            trace.line != null &&
            'color' in trace.line &&
            typeof trace.line.color === 'string') {
            if (plotlyColors.has(trace.line.color.toUpperCase())) {
                trace.line.color = colorMap.get(trace.line.color.toUpperCase());
            }
        }
    }
}
//# sourceMappingURL=PlotlyExpressChartUtils.js.map
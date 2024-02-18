export function ErddapService(): {
    generateDataUrl(datasetId: number, variables: Array<any>, fileFormat: string, dateRange?: any): string; 
    generateMetadataUrl(datasetId: number, fileFormat: string): string;
    percentEncode(s: string): string;
};

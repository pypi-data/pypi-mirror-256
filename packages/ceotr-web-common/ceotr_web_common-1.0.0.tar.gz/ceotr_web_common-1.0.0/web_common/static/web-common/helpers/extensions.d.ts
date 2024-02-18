interface DateConstructor {
    getShortTimezone: () => string;
    getLongTimezone: () => string;
}
interface String {
    equalsIgnoreCase: (second: string) => boolean;
}
interface ArrayConstructor {
    indexOfByProperty: (arr: Array<any>, val: any, property: string) => number;
    getByProperty: (arr: Array<any>, val: any, property: string) => any;
    unique: <T>(arr: Array<T>, key: any) => Array<T>;
    contains: (arr: Array<any>, val: any) => boolean;
}

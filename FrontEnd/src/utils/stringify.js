export function simpleStringify (object){
    var cache = [];
    var str = JSON.stringify(object, function(key, value) {
        if (typeof value === 'object' && value !== null) {
            if (cache.indexOf(value) !== -1) {
                // remove the value
                return;
            }
            // collect all values
            cache.push(value);
        }
        return value;
    });
    cache = null;
    return str
};
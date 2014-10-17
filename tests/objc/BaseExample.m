#import "BaseExample.h"

@implementation BaseExample;

static int _staticBaseIntField = 1;

+(int) staticBaseIntField
{
    @synchronized(self)
    {
        return _staticBaseIntField;
    }
}

+(void) setStaticBaseIntField: (int) v
{
    @synchronized(self)
    {
        _staticBaseIntField = v;
    }
}

+(int) accessStaticBaseIntField
{
    @synchronized(self) {
        return _staticBaseIntField;
    }
}

+(void) mutateStaticBaseIntFieldWithValue: (int) v
{
    @synchronized(self) {
        _staticBaseIntField = v;
    }
}

-(id) init
{
    self = [super init];

    if (self) {
        [self setBaseIntField:2];
    }
    return self;
}

-(id) initWithIntValue: (int) v
{
    self = [super init];

    if (self) {
        [self setBaseIntField:v];
    }
    return self;
}


-(int) accessBaseIntField
{
    return self.baseIntField;
}

-(void) mutateBaseIntFieldWithValue: (int) v
{
    self.baseIntField = v;
}

@end
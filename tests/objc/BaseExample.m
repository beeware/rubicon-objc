#import "BaseExample.h"

@implementation BaseExample

@synthesize baseIntField = _baseIntField;

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


-(void) method:(int) v withArg: (int) m{
    self.baseIntField = v * m;
}

-(void) methodWithArgs: (int) num, ... {

   int sum = 0;

   va_list args;
   va_start( args, num );

   for( int i = 0; i < num; i++)
   {
      sum += va_arg( args, int);
   }

   va_end( args );

   self.baseIntField = sum;
}

-(void) method:(int) v{
    self.baseIntField = v;
}

@end

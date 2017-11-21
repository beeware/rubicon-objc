#import "Thing.h"

@implementation Thing

@synthesize name = _name;

-(id) initWithName: (NSString *) name
{
    self = [super init];

    if (self) {
        self.name = name;
    }
    return self;
}

-(id) initWithName: (NSString *) name value: (int) v
{
    self = [super init];

    if (self) {
        self.name = [NSString stringWithFormat:@"%@ %d", name, v, NULL];
    }
    return self;
}

-(NSString *) toString
{
    return self.name;
}

-(NSSize) computeSize: (NSSize) input
{
    printf("THING COMPUTE %f %f\n", input.width, input.height);
    return NSMakeSize(input.width * 2, input.height * 3);
}

@end
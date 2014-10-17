#import "Thing.h"

@implementation Thing;

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

@end
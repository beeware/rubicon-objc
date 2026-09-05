#import "DescriptionTester.h"

@implementation DescriptionTester

@synthesize descriptionString = _descriptionString;
@synthesize debugDescriptionString = _debugDescriptionString;

-(instancetype) initWithDescriptionString:(NSString *)descriptionString debugDescriptionString:(NSString *)debugDescriptionString {
    self = [super init];
    if (self) {
        self.descriptionString = descriptionString;
        self.debugDescriptionString = debugDescriptionString;
    }
    return self;
}

-(NSString *) description {
    return self.descriptionString;
}

-(NSString *) debugDescription {
    return self.debugDescriptionString;
}

@end

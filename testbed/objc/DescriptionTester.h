#import <Foundation/Foundation.h>

@interface DescriptionTester : NSObject {
    NSString *_descriptionString;
    NSString *_debugDescriptionString;
}

@property (retain) NSString *descriptionString;
@property (retain) NSString *debugDescriptionString;

-(instancetype) initWithDescriptionString:(NSString *)descriptionString debugDescriptionString:(NSString *)debugDescriptionString;

@end

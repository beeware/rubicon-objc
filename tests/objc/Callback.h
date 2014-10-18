#import <Foundation/Foundation.h>

@class Example;

@protocol Callback

- (void) poke: (Example *) example withValue: (int) value;
- (void) peek: (Example *) example withValue: (int) value;
- (NSString *) reverse: (NSString *) input;
- (NSString *) message;

@end
#import <Foundation/Foundation.h>

@protocol ExampleProtocol @end

@protocol BaseProtocolOne @end

@protocol BaseProtocolTwo @end

@protocol DerivedProtocol <BaseProtocolOne, BaseProtocolTwo> @end

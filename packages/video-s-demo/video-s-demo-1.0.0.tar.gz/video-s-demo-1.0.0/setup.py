from setuptools import setup 

# reading long description from file 
with open('README.md') as file: 
	long_description = file.read() 


# specify requirements of your package here 
REQUIREMENTS = ['requests'] 

# some more details 
CLASSIFIERS = [ 
	'Programming Language :: Python', 
	'Programming Language :: Python :: 3', 
	'Programming Language :: Python :: 3.10', 
	] 

# calling the setup function 
setup(name='video-s-demo', 
	version='1.0.0', 
	description='A package for video summarization', 
	long_description=long_description,
	url='https://github.com/HieuTrungCao/Video_Summarization.git', 
	author='Cao Trung Hieu, Trinh Duc Hiep', 
	author_email='hieuhocao@gmail.com, 21020169@vnu.edu.vn', 
	license='MIT',
	classifiers=CLASSIFIERS, 
	install_requires=REQUIREMENTS,
	long_description_content_type="text/markdown"
	) 


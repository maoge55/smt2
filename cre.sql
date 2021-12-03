USE [smt]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[class](
	[cid] [int] IDENTITY(1,1) NOT NULL,
	[cname] [nvarchar](255) NOT NULL,
	[curl] [nvarchar](max) NULL,
	[grade] [int] NULL,
	[cfid] [int] NULL,
	[cfname] [nvarchar](255) NULL,
	[cstate] [int] NULL,
	[cpage] [int] NULL,
	[cpcount] [nvarchar](255) NULL,
 CONSTRAINT [un_id_time] UNIQUE NONCLUSTERED 
(
	[cname] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

ALTER TABLE [dbo].[class] ADD  CONSTRAINT [DF_TB_Class_cstate]  DEFAULT ((0)) FOR [cstate]
GO

ALTER TABLE [dbo].[class] ADD  CONSTRAINT [DF_class_cpage]  DEFAULT ((60)) FOR [cpage]
GO

CREATE TABLE [dbo].[pids](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[pid] [nvarchar](50) NOT NULL,
	[url] [nvarchar](max) NULL,
	[pcid] [int] NOT NULL,
	[pstate] [int] NULL,
 CONSTRAINT [PK_pids] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY],
 CONSTRAINT [IX_pids] UNIQUE NONCLUSTERED 
(
	[pid] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

ALTER TABLE [dbo].[pids] ADD  CONSTRAINT [DF_pids_pstate]  DEFAULT ((0)) FOR [pstate]
GO

CREATE TABLE [dbo].[product](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[pid] [nvarchar](100) NOT NULL,
	[pcid] [int] NOT NULL,
	[pname] [nvarchar](500) NULL,
	[psku] [text] NULL,
	[pprice] [text] NULL,
	[pprint] [text] NULL,
	[pseo] [text] NULL,
	[pdec] [text] NULL,
	[pon] [int] NOT NULL,
 CONSTRAINT [PK_product] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY],
 CONSTRAINT [IX_product] UNIQUE NONCLUSTERED 
(
	[pid] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO

ALTER TABLE [dbo].[product] ADD  CONSTRAINT [DF_product_pon]  DEFAULT ((1)) FOR [pon]
GO

